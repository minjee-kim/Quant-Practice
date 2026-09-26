"""Quiz timing and scoring, independent of the webpage."""

import time

from questions import make_questions


SECONDS_PER_QUESTION = 60
FEEDBACK_SECONDS = 2.5


def new_quiz(now=None):
    return {
        "questions": make_questions(),
        "index": 0,
        "started_at": time.monotonic() if now is None else now,
        "phase": "question",
        "results": [],
        "feedback_until": None,
    }


def submit(quiz, selected, now=None):
    """Record a single answer; a submission after the deadline times out."""
    if quiz["phase"] != "question":
        return None
    now = time.monotonic() if now is None else now
    elapsed = max(0.0, now - quiz["started_at"])
    timed_out = elapsed >= SECONDS_PER_QUESTION
    question = quiz["questions"][quiz["index"]]
    result = {
        "number": quiz["index"] + 1,
        "topic": question["topic"],
        "kind": question["kind"],
        "prompt": question["prompt"],
        "selected": None if timed_out else selected,
        "answer": question["answer"],
        "correct": not timed_out and selected == question["answer"],
        "timed_out": timed_out,
        "seconds": round(min(elapsed, SECONDS_PER_QUESTION), 1),
        "solution": question["solution"],
    }
    quiz["results"].append(result)
    quiz["phase"] = "feedback"
    quiz["feedback_until"] = now + FEEDBACK_SECONDS
    return result


def advance(quiz, now=None):
    if quiz["phase"] != "feedback":
        return
    quiz["index"] += 1
    if quiz["index"] == len(quiz["questions"]):
        quiz["phase"] = "finished"
    else:
        quiz["phase"] = "question"
        quiz["started_at"] = time.monotonic() if now is None else now
    quiz["feedback_until"] = None
