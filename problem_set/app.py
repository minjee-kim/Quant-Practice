"""Run from the repo root: python3 -m streamlit run problem_set/app.py"""

import csv
import io
import math
import re
import time
from fractions import Fraction

import streamlit as st

from engine import advance, compatible_quiz, new_quiz, submit
from questions import (CATEGORIES, DISTRIBUTION_FAMILIES, LEVEL_SECONDS,
                       eligible_templates)


st.set_page_config(page_title="Quant Practice | Problem Set", page_icon="🧠")
st.title("Quant Practice · Problem Set")
st.caption("Theory and mental math · Pick what to practice")


def display_choice(value):
    """Use compact inline math so radio choices keep comfortable spacing."""
    if value is None:
        return "Time expired"
    if isinstance(value, str) and value.startswith("$") and value.endswith("$"):
        return value
    if isinstance(value, str) and re.fullmatch(r"-?\d+\.\d+", value):
        return f"${value}$"
    try:
        number = Fraction(value)
    except (ValueError, TypeError, ZeroDivisionError):
        return str(value).replace("$", r"\$")
    if number.denominator == 1:
        return f"${number.numerator}$"
    return f"${number.numerator}/{number.denominator}$"


def attribution(item):
    label = f"{item['source_relation']} {item['source_name']}"
    if item["source_url"]:
        return f"{item['source_relation']} [{item['source_name']}]({item['source_url']})"
    return label


def score_table(results, field, title):
    rows = []
    for name in dict.fromkeys(row[field] for row in results):
        if name is None:
            continue
        matching = [row for row in results if row[field] == name]
        correct = sum(row["correct"] for row in matching)
        rows.append({title: name, "Correct": correct, "Total": len(matching)})
    if rows:
        st.table(rows)


def results_csv(results):
    output = io.StringIO()
    fields = ["number", "category", "family", "topic", "level", "seconds_limit",
              "kind", "prompt", "selected", "answer", "correct", "timed_out",
              "seconds", "solution",
              "source_name", "source_url", "source_relation"]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    writer.writerows(results)
    return output.getvalue()


@st.fragment(run_every="0.5s")
def drill():
    quiz = st.session_state.quiz
    now = time.monotonic()
    if quiz["phase"] == "question":
        limit = quiz["questions"][quiz["index"]]["seconds_limit"]
        if now - quiz["started_at"] >= limit:
            submit(quiz, None, now)
    if quiz["phase"] == "feedback" and now >= quiz["feedback_until"]:
        advance(quiz, now)

    if quiz["phase"] == "finished":
        results = quiz["results"]
        score = sum(result["correct"] for result in results)
        st.header("Your results")
        cols = st.columns(3)
        cols[0].metric("Correct", f"{score} / {len(results)}")
        cols[1].metric("Average time", f"{sum(r['seconds'] for r in results) / len(results):.1f}s")
        cols[2].metric("Timed out", sum(r["timed_out"] for r in results))
        breakdown, review, export = st.tabs(("Breakdown", "Review answers", "Download"))
        with breakdown:
            st.subheader("By topic")
            score_table(results, "category", "Topic")
            if any(r["family"] for r in results):
                st.subheader("By distribution family")
                score_table(results, "family", "Family")
            st.subheader("By question type")
            score_table(results, "topic", "Question type")
            st.subheader("By level")
            score_table(results, "level", "Level")
        with review:
            review_filter = st.radio("Show", ("All", "Incorrect", "Timed out"),
                                     horizontal=True)
            shown = [r for r in results
                     if review_filter == "All"
                     or review_filter == "Incorrect" and not r["correct"]
                     or review_filter == "Timed out" and r["timed_out"]]
            if not shown:
                st.info("No questions in this group.")
            for result in shown:
                marker = "✓" if result["correct"] else "✗"
                with st.expander(f"{marker} Question {result['number']}: {result['kind']}"):
                    family = f" · {result['family']}" if result["family"] else ""
                    st.caption(f"{result['category']}{family} · {result['level']} · "
                               f"{result['seconds']:.1f}s / {result['seconds_limit']}s")
                    st.markdown(result["prompt"])
                    st.markdown(f"Your answer: {display_choice(result['selected'])}")
                    st.markdown(f"Correct answer: {display_choice(result['answer'])}")
                    st.markdown(result["solution"])
                    st.caption(attribution(result))
        with export:
            st.write("Save your responses, solutions, timing, and source links.")
            st.download_button("Download results as CSV", data=results_csv(results),
                               file_name="quant_practice_results.csv", mime="text/csv")
        restart, change = st.columns(2)
        if restart.button("Try same setup", use_container_width=True):
            st.session_state.quiz = new_quiz(**quiz["settings"])
            st.rerun()
        if change.button("Change setup", use_container_width=True):
            del st.session_state.quiz
            st.rerun()
        return

    index = quiz["index"]
    question = quiz["questions"][index]
    st.progress((index + 1) / len(quiz["questions"]),
                text=f"Question {index + 1} of {len(quiz['questions'])}")
    family = f" · {question['family']}" if question["family"] else ""
    st.caption(f"{question['category']}{family} · {question['level']} "
               f"({question['seconds_limit']} seconds)")
    st.subheader(question["kind"])
    st.markdown(question["prompt"])
    st.caption(attribution(question))

    if quiz["phase"] == "question":
        seconds_left = max(0, math.ceil(question["seconds_limit"] - (now - quiz["started_at"])))
        st.metric("Time remaining", f"{seconds_left // 60}:{seconds_left % 60:02d}")
        selected = st.radio("Choose one answer", question["choices"],
                            format_func=display_choice,
                            index=None, key=f"choice_{index}")
        if st.button("Submit answer", type="primary", disabled=selected is None,
                     shortcut="Enter"):
            submit(quiz, selected, time.monotonic())
            st.rerun()
    else:
        result = quiz["results"][-1]
        for option in question["choices"]:
            if option == question["answer"]:
                st.success(f"✓ {display_choice(option)}")
            elif option == result["selected"]:
                st.error(f"✗ {display_choice(option)}")
            else:
                st.markdown(f"○ {display_choice(option)}")
        if result["timed_out"]:
            st.warning("Time expired.")
        elif result["correct"]:
            st.success("Correct!")
        else:
            st.error("Incorrect.")
        st.caption("Next question starts automatically in a moment.")
        if st.button("Continue now", shortcut="Enter"):
            advance(quiz, time.monotonic())
            st.rerun()


if "quiz" in st.session_state and not compatible_quiz(st.session_state.quiz):
    del st.session_state.quiz
    for key in list(st.session_state):
        if key.startswith("choice_"):
            del st.session_state[key]
    st.info("The question bank changed, so your saved round was reset. Start a new set below.")

if "quiz" not in st.session_state:
    st.write("Timed theory questions and mental math with worked answers.")
    st.subheader("Build your set")
    category = tuple(st.multiselect("Topics", CATEGORIES, default=CATEGORIES,
                                    help="Keep all selected for a mixed set, or select a subset."))
    if "Distributions" in category:
        families = tuple(st.multiselect(
            "Distribution families", DISTRIBUTION_FAMILIES,
            default=DISTRIBUTION_FAMILIES,
            help="Uniform means continuous Uniform; dice are grouped separately."))
    else:
        families = tuple(DISTRIBUTION_FAMILIES)
    levels = ("Mixed",) + tuple(level for level in LEVEL_SECONDS
                                 if eligible_templates(category, level, families))
    level_col, length_col = st.columns(2)
    with level_col:
        level = st.selectbox("Level", levels,
                             help="Mixed uses each question's own time limit.")
    pool = eligible_templates(category, level, families)
    lengths = [5]
    if len(pool) >= 4:
        lengths.append(10)
    if len(pool) >= 15:
        lengths.append(15)
    with length_col:
        count = st.selectbox("Questions", lengths,
                             index=lengths.index(10) if 10 in lengths else 0)
    valid = bool(pool) and ("Distributions" not in category or bool(families))
    if not category:
        st.warning("Select at least one topic.")
    elif "Distributions" in category and not families:
        st.warning("Choose at least one distribution family, or remove Distributions.")
    else:
        st.caption(f"{len(pool)} question types · Level 1: 60s · Level 2: 120s "
                   "· Level 3: 180s. Focused sets may repeat a type with new values.")
    if st.button(f"Start {count}-question set", type="primary", disabled=not valid,
                 use_container_width=True):
        st.session_state.quiz = new_quiz(count=count, category=category,
                                         level=level, families=families)
        st.rerun()
else:
    drill()

with st.expander("Question sources and interview guides"):
    st.markdown(
        "**Published exercises adapted for this quiz**\n\n"
        "- [Jane Street — Probability & Markets](https://www.janestreet.com/static/pdfs/trading-interview.pdf): "
        "probability, expected value, and markets.\n"
        "- [Susquehanna — Game Theory + Decision Science](https://sig.com/who-we-are/game-theory-decision-science/): "
        "conditional rates and independent coin flips.\n\n"
        "Uniform, Normal, and additional Binomial questions are original exercises "
        "using [NIST's distribution reference](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366.htm) "
        "for formulas. Mental math drills are original. These are not claimed "
        "to be real interview questions.\n\n"
        "**Firm interview guidance** (these pages do not provide the quiz questions)\n\n"
        "- [Citadel — Quantitative Research Interview Process](https://www.citadel.com/careers/career-perspectives/our-quantitative-research-interview-process/): "
        "programming, research, algorithms, and explaining your approach.\n"
        "- [Citadel — Quantitative Research FAQs](https://www.citadel.com/careers/career-perspectives/candidate-faqs-quantitative-research/): "
        "statistics, coding, predictive models, and working with data.\n"
        "- [Two Sigma — Interviewing for Quantitative Research & Modeling](https://www.twosigma.com/interviewing-for-quantitative-research-modeling/): "
        "data analysis, coding, statistics, and a mock interview video.\n"
        "- [Optiver — Quant Research internship story](https://www.optiver.com/join-us/stories/from-computer-science-to-quant-research-lucys-internship-story/): "
        "an account of an open-ended, data-based interview project.\n"
        "- [IMC — How to prepare for an interview](https://www.imc.com/ap/articles/how-to-prepare-for-an-interview-at-imc): "
        "technical problem solving with an interviewer."
    )
