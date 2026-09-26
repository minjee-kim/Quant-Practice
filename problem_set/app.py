"""Run from the repo root: python3 -m streamlit run problem_set/app.py"""

import csv
import io
import math
import time

import streamlit as st

from engine import SECONDS_PER_QUESTION, advance, new_quiz, submit


st.set_page_config(page_title="Quant Practice | Problem Set", page_icon="🧠")
st.title("Quant Practice · Problem Set")
st.caption("Ten randomized questions · 60 seconds each · Enter to submit")


def results_csv(results):
    output = io.StringIO()
    fields = ["number", "topic", "kind", "prompt", "selected", "answer",
              "correct", "timed_out", "seconds", "solution"]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    writer.writerows(results)
    return output.getvalue()


@st.fragment(run_every="0.5s")
def drill():
    quiz = st.session_state.quiz
    now = time.monotonic()
    if quiz["phase"] == "question" and now - quiz["started_at"] >= SECONDS_PER_QUESTION:
        submit(quiz, None, now)
    if quiz["phase"] == "feedback" and now >= quiz["feedback_until"]:
        advance(quiz, now)

    if quiz["phase"] == "finished":
        results = quiz["results"]
        score = sum(result["correct"] for result in results)
        st.header(f"Result: {score} / {len(results)}")
        st.write(f"Average response time: {sum(r['seconds'] for r in results) / len(results):.1f} seconds")
        st.subheader("By topic")
        for topic in dict.fromkeys(r["topic"] for r in results):
            matching = [r for r in results if r["topic"] == topic]
            st.write(f"{topic}: {sum(r['correct'] for r in matching)} / {len(matching)}")
        st.subheader("Review")
        for result in results:
            marker = "✓" if result["correct"] else "✗"
            with st.expander(f"{marker} Question {result['number']}: {result['kind']}"):
                st.write(result["prompt"])
                st.write(f"Your answer: {result['selected'] or 'Time expired'}")
                st.write(f"Correct answer: {result['answer']}")
                st.write(result["solution"])
        st.download_button("Download results as CSV", data=results_csv(results),
                           file_name="quant_practice_results.csv", mime="text/csv")
        if st.button("Try another set"):
            st.session_state.quiz = new_quiz()
            st.rerun()
        return

    index = quiz["index"]
    question = quiz["questions"][index]
    st.progress((index + 1) / len(quiz["questions"]),
                text=f"Question {index + 1} of {len(quiz['questions'])}")
    st.caption(f"{question['topic']} · {question['kind']}")
    st.subheader(question["prompt"])

    if quiz["phase"] == "question":
        seconds_left = max(0, math.ceil(SECONDS_PER_QUESTION - (now - quiz["started_at"])))
        st.metric("Time remaining", f"0:{seconds_left:02d}")
        selected = st.radio("Choose one answer", question["choices"],
                            index=None, key=f"choice_{index}")
        if st.button("Submit answer", type="primary", disabled=selected is None,
                     shortcut="Enter"):
            submit(quiz, selected, time.monotonic())
            st.rerun()
    else:
        result = quiz["results"][-1]
        for option in question["choices"]:
            if option == question["answer"]:
                st.success(f"✓ {option}")
            elif option == result["selected"]:
                st.error(f"✗ {option}")
            else:
                st.write(f"○ {option}")
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


if "quiz" not in st.session_state:
    st.write("Practice mental math, probability, expected value, combinatorics, and Bayes' rule.")
    st.write("Each set has two questions from each topic. Numbers and choices change every time.")
    if st.button("Start 10-question set", type="primary"):
        st.session_state.quiz = new_quiz()
        st.rerun()
else:
    drill()
