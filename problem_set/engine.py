"""Quiz timing and scoring, independent of the webpage."""

import time

from questions import make_questions


def compatible_quiz(quiz):
    """Reject rounds saved before untimed practice became the default."""
    if not isinstance(quiz, dict):
        return False
    questions = quiz.get("questions")
    results = quiz.get("results")
    phase = quiz.get("phase")
    index = quiz.get("index")
    if (not isinstance(questions, list) or not questions
            or not isinstance(results, list)
            or phase not in {"question", "finished"}
            or not isinstance(index, int)
            or not 0 <= index <= len(questions)
            or not isinstance(quiz.get("timed"), bool)):
        return False
    question_fields = {"topic", "category", "family", "level", "seconds_limit",
                       "kind", "prompt", "answer", "choices", "solution",
                       "source_name", "source_url", "source_relation"}
    result_fields = {"number", "topic", "category", "family", "level", "seconds_limit",
                     "kind", "prompt", "selected",
                     "answer", "correct", "timed_out", "seconds", "solution",
                     "source_name", "source_url", "source_relation"}
    return (all(isinstance(q, dict) and question_fields <= q.keys()
                for q in questions)
            and all(isinstance(r, dict) and result_fields <= r.keys()
                    for r in results))


def new_quiz(now=None, timed=False):
    return {
        "questions": make_questions(count=10),
        "timed": timed,
        "index": 0,
        "started_at": time.monotonic() if now is None else now,
        "phase": "question",
        "results": [],
    }


def submit(quiz, selected, now=None):
    """Record an answer and move on; only timed rounds can expire."""
    if quiz["phase"] != "question":
        return None
    now = time.monotonic() if now is None else now
    elapsed = max(0.0, now - quiz["started_at"])
    question = quiz["questions"][quiz["index"]]
    limit = question["seconds_limit"] if quiz["timed"] else None
    timed_out = limit is not None and elapsed >= limit
    result = {
        "number": quiz["index"] + 1,
        "topic": question["topic"],
        "category": question["category"],
        "family": question["family"],
        "level": question["level"],
        "seconds_limit": limit,
        "kind": question["kind"],
        "prompt": question["prompt"],
        "selected": None if timed_out else selected,
        "answer": question["answer"],
        "correct": not timed_out and selected == question["answer"],
        "timed_out": timed_out,
        "seconds": round(min(elapsed, limit), 1) if limit is not None else None,
        "solution": question["solution"],
        "source_name": question["source_name"],
        "source_url": question["source_url"],
        "source_relation": question["source_relation"],
    }
    quiz["results"].append(result)
    quiz["index"] += 1
    if quiz["index"] == len(quiz["questions"]):
        quiz["phase"] = "finished"
    else:
        quiz["started_at"] = now
    return result
