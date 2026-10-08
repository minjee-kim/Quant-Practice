"""Run from the repo root: python3 -m streamlit run problem_set/app.py"""

import csv
import datetime
import io
import math
import re
import time
from fractions import Fraction

import streamlit as st

from engine import compatible_quiz, new_quiz, submit
from review import TOPICS, topic_for


st.set_page_config(page_title="Quant Practice", page_icon="🧠")
st.title("Quant Practice")


def display_choice(value):
    """Render a choice without reducing it. (1/3)^8 must not become 1/6561."""
    if value is None:
        return "Time expired"
    text = str(value)
    if text.startswith("$") and text.endswith("$"):
        return text
    if re.fullmatch(r"-?\d+/\d+", text):
        return f"${text}$"
    if re.fullmatch(r"-?\d+\.\d+", text):
        return f"${text}$"
    try:
        number = Fraction(text)
    except (ValueError, TypeError, ZeroDivisionError):
        return text.replace("$", r"\$")
    if number.denominator == 1:
        return f"${number.numerator}$"
    return f"${number.numerator}/{number.denominator}$"


def attribution(item):
    if item["source_url"]:
        return f"{item['source_relation']} [{item['source_name']}]({item['source_url']})"
    return f"{item['source_relation']} {item['source_name']}"


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
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(results)
    return output.getvalue()


def start_quiz(**kwargs):
    st.session_state.quiz = new_quiz(**kwargs)
    st.rerun()


def drill():
    quiz = st.session_state.quiz
    now = time.monotonic()
    if quiz["phase"] == "question" and quiz["timed"]:
        limit = quiz["questions"][quiz["index"]]["seconds_limit"]
        if now - quiz["started_at"] >= limit:
            submit(quiz, None, now)

    if quiz["phase"] == "finished":
        results = quiz["results"]
        score = sum(result["correct"] for result in results)
        st.header(f"Result: {score} / {len(results)}")
        if quiz.get("title"):
            st.caption(quiz["title"] + " · done for today")
        if quiz["timed"]:
            st.caption(f"Average response: {sum(r['seconds'] for r in results) / len(results):.1f}s "
                       f"· Timed out: {sum(r['timed_out'] for r in results)}")
        st.subheader("By topic")
        score_table(results, "category", "Topic")
        if any(r["family"] for r in results):
            st.subheader("By distribution")
            score_table(results, "family", "Distribution")
        st.subheader("Review answers")
        for result in results:
            marker = "✓" if result["correct"] else "✗"
            with st.expander(f"{marker} Question {result['number']}: {result['kind']}"):
                st.markdown(result["prompt"])
                st.markdown(f"Your answer: {display_choice(result['selected'])}")
                st.markdown(f"Correct answer: {display_choice(result['answer'])}")
                st.markdown(result["solution"])
                st.caption(attribution(result))
        st.download_button("Download results (CSV)", data=results_csv(results),
                           file_name="quant_practice_results.csv", mime="text/csv")
        if st.button("Back", type="primary", use_container_width=True):
            del st.session_state.quiz
            st.rerun()
        return

    index = quiz["index"]
    question = quiz["questions"][index]
    if quiz.get("title"):
        st.caption(quiz["title"])
    st.progress((index + 1) / len(quiz["questions"]),
                text=f"Question {index + 1} of {len(quiz['questions'])}")
    st.subheader(question["kind"])
    st.markdown(question["prompt"])
    if quiz["timed"]:
        seconds_left = max(0, math.ceil(question["seconds_limit"] - (now - quiz["started_at"])))
        st.metric("Time remaining", f"{seconds_left // 60}:{seconds_left % 60:02d}")
    selected = st.radio("Choose one answer", question["choices"],
                        format_func=display_choice,
                        index=None, key=f"choice_{index}")
    if st.button("Submit answer", type="primary", disabled=selected is None,
                 shortcut="Enter", use_container_width=True):
        submit(quiz, selected, time.monotonic())
        st.rerun()


@st.fragment(run_every="0.5s")
def timed_drill():
    drill()


def home():
    today = datetime.date.today()
    card = topic_for(today.toordinal())
    st.subheader(card["title"])
    st.markdown(card["say"])
    st.caption("Trap: " + card["trap"])
    if st.button("Start today's 5", type="primary", use_container_width=True):
        start_quiz(count=5, category=card["category"], seed=today.toordinal(),
                   title=card["title"])
    timed = st.toggle("Use a timer", value=False,
                      help="Optional on the mixed set: 1 to 3 minutes by difficulty.")
    if st.button("Mixed 10 instead", use_container_width=True):
        start_quiz(timed=timed, count=10, title="Mixed 10")
    st.divider()
    st.subheader("Topic list")
    for item in TOPICS:
        st.markdown(f"**{item['title']}**")
        st.markdown(item["say"])
        if st.button(f"Drill {item['title']}", key=f"drill_{item['key']}",
                     use_container_width=True):
            start_quiz(count=5, category=item["category"],
                       seed=today.toordinal() + TOPICS.index(item),
                       title=item["title"])


if "quiz" in st.session_state and not compatible_quiz(st.session_state.quiz):
    del st.session_state.quiz
    for key in list(st.session_state):
        if key.startswith("choice_"):
            del st.session_state[key]

if "quiz" not in st.session_state:
    home()
else:
    if st.session_state.quiz["timed"] and st.session_state.quiz["phase"] == "question":
        timed_drill()
    else:
        drill()
