"""Run from the repo root: python3 -m streamlit run problem_set/app.py"""

import csv
import io
import math
import time
from fractions import Fraction

import streamlit as st

from engine import advance, compatible_quiz, new_quiz, submit
from questions import CATEGORIES, LEVEL_SECONDS, eligible_templates


st.set_page_config(page_title="Quant Practice | Problem Set", page_icon="🧠")
st.title("Quant Practice · Problem Set")
st.caption("Source-linked practice · Choose a topic, level, and set length")


def display_choice(value):
    """Use compact inline math so radio choices keep comfortable spacing."""
    if value is None:
        return "Time expired"
    try:
        number = Fraction(value)
    except (ValueError, TypeError, ZeroDivisionError):
        return str(value).replace("$", r"\$")
    if number.denominator == 1:
        return f"${number.numerator}$"
    return f"${number.numerator}/{number.denominator}$"


def results_csv(results):
    output = io.StringIO()
    fields = ["number", "category", "topic", "level", "seconds_limit",
              "kind", "prompt", "selected", "answer", "correct", "timed_out",
              "seconds", "solution",
              "source_name", "source_url"]
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
        st.header(f"Result: {score} / {len(results)}")
        st.write(f"Average response time: {sum(r['seconds'] for r in results) / len(results):.1f} seconds")
        st.write(f"Timed out: {sum(r['timed_out'] for r in results)}")
        st.subheader("By category")
        for category in dict.fromkeys(r["category"] for r in results):
            matching = [r for r in results if r["category"] == category]
            st.write(f"{category}: {sum(r['correct'] for r in matching)} / {len(matching)}")
        st.subheader("By topic")
        for topic in dict.fromkeys(r["topic"] for r in results):
            matching = [r for r in results if r["topic"] == topic]
            st.write(f"{topic}: {sum(r['correct'] for r in matching)} / {len(matching)}")
        st.subheader("By level")
        for level in LEVEL_SECONDS:
            matching = [r for r in results if r["level"] == level]
            if matching:
                st.write(f"{level}: {sum(r['correct'] for r in matching)} / {len(matching)}")
        st.subheader("Review")
        for result in results:
            marker = "✓" if result["correct"] else "✗"
            with st.expander(f"{marker} Question {result['number']}: {result['kind']}"):
                st.caption(f"{result['category']} · {result['level']} · "
                           f"{result['seconds']:.1f}s / {result['seconds_limit']}s")
                st.markdown(result["prompt"])
                st.markdown(f"Your answer: {display_choice(result['selected'])}")
                st.markdown(f"Correct answer: {display_choice(result['answer'])}")
                st.markdown(result["solution"])
                st.markdown(f"Source: [{result['source_name']}]({result['source_url']})")
        st.download_button("Download results as CSV", data=results_csv(results),
                           file_name="quant_practice_results.csv", mime="text/csv")
        if st.button("Try same setup"):
            st.session_state.quiz = new_quiz(**quiz["settings"])
            st.rerun()
        if st.button("Change setup"):
            del st.session_state.quiz
            st.rerun()
        return

    index = quiz["index"]
    question = quiz["questions"][index]
    st.progress((index + 1) / len(quiz["questions"]),
                text=f"Question {index + 1} of {len(quiz['questions'])}")
    st.caption(f"{question['category']} · {question['topic']} · "
               f"{question['level']} ({question['seconds_limit']} seconds)")
    st.subheader("Question")
    st.markdown(question["prompt"])
    st.caption(f"Adapted from [{question['source_name']}]({question['source_url']}).")

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
    st.write("Practice probability, distributions, expected value, markets, "
             "and data interpretation with fresh numbers and worked solutions.")
    st.caption("The exercises adapt published Jane Street and Susquehanna examples. "
               "They are not verified transcripts of live interviews.")
    st.subheader("Build your set")
    topic_mode = st.selectbox("Topic", ("Mixed",) + CATEGORIES + ("Custom mix",))
    if topic_mode == "Custom mix":
        category = tuple(st.multiselect("Choose topics", CATEGORIES,
                                        default=CATEGORIES[:2]))
    else:
        category = topic_mode
    levels = ("Mixed",) + tuple(level for level in LEVEL_SECONDS
                                 if eligible_templates(category, level))
    level = st.selectbox("Level", levels)
    pool = eligible_templates(category, level)
    lengths = [5]
    if len(pool) >= 4:
        lengths.append(10)
    if len(pool) >= 15:
        lengths.append(15)
    count = st.selectbox("Questions per set", lengths,
                         index=lengths.index(10) if 10 in lengths else 0)
    st.caption("Level 1: 60 seconds · Level 2: 120 seconds · Level 3: 180 seconds. "
               "Mixed levels use each question's own timer. Focused sets may revisit "
               "a type with new values.")
    if not pool:
        st.warning("Choose at least one topic.")
    else:
        st.caption(f"{len(pool)} question types match this selection.")
    if st.button(f"Start {count}-question set", type="primary", disabled=not pool):
        st.session_state.quiz = new_quiz(count=count, category=category, level=level)
        st.rerun()
else:
    drill()

with st.expander("Official interview guides and further practice"):
    st.markdown(
        "**Published exercises used in this quiz**\n\n"
        "- [Jane Street — Probability & Markets](https://www.janestreet.com/static/pdfs/trading-interview.pdf): "
        "probability, expected value, and markets.\n"
        "- [Susquehanna — Game Theory + Decision Science](https://sig.com/who-we-are/game-theory-decision-science/): "
        "conditional rates and independent coin flips.\n\n"
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
