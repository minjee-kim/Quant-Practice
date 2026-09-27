"""Quiz timing and scoring, independent of the webpage."""

import time

from questions import make_questions


FEEDBACK_SECONDS = 2.5


def compatible_quiz(quiz):
    """Reject saved rounds from the earlier, unsourced question bank."""
    if not isinstance(quiz, dict):
        return False
    questions = quiz.get("questions")
    results = quiz.get("results")
    phase = quiz.get("phase")
    index = quiz.get("index")
    if (not isinstance(questions, list) or not questions
            or not isinstance(results, list)
            or phase not in {"question", "feedback", "finished"}
            or not isinstance(index, int)
            or not 0 <= index <= len(questions)):
        return False
    question_fields = {"topic", "category", "level", "seconds_limit",
                       "kind", "prompt", "answer", "choices", "solution",
                       "source_name", "source_url"}
    result_fields = {"number", "topic", "category", "level", "seconds_limit",
                     "kind", "prompt", "selected",
                     "answer", "correct", "timed_out", "seconds", "solution",
                     "source_name", "source_url"}
    return (all(isinstance(q, dict) and question_fields <= q.keys()
                for q in questions)
            and all(isinstance(r, dict) and result_fields <= r.keys()
                    for r in results)
            and isinstance(quiz.get("settings"), dict))


def new_quiz(now=None, count=10, category="Mixed", level="Mixed"):
    return {
        "questions": make_questions(count=count, category=category, level=level),
        "settings": {"count": count, "category": category, "level": level},
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
    question = quiz["questions"][quiz["index"]]
    limit = question["seconds_limit"]
    timed_out = elapsed >= limit
    result = {
        "number": quiz["index"] + 1,
        "topic": question["topic"],
        "category": question["category"],
        "level": question["level"],
        "seconds_limit": limit,
        "kind": question["kind"],
        "prompt": question["prompt"],
        "selected": None if timed_out else selected,
        "answer": question["answer"],
        "correct": not timed_out and selected == question["answer"],
        "timed_out": timed_out,
        "seconds": round(min(elapsed, limit), 1),
        "solution": question["solution"],
        "source_name": question["source_name"],
        "source_url": question["source_url"],
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
