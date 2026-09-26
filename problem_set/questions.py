"""Question generators. Add a function to GENERATORS to add a question type."""

import math
import random
from fractions import Fraction


def choices(answer, wrong, rng):
    options = [answer]
    for value in wrong:
        if value not in options:
            options.append(value)
        if len(options) == 4:
            break
    if len(options) != 4:
        raise ValueError("Need three distinct distractors")
    rng.shuffle(options)
    return options


def percentage(rng):
    p = rng.choice([5, 10, 15, 20, 25, 30, 35, 40])
    n = rng.choice([40, 80, 120, 160, 200, 240, 400])
    answer = str(p * n // 100)
    return {
        "topic": "Mental math", "kind": "Percentages",
        "prompt": f"What is {p}% of {n}?", "answer": answer,
        "choices": choices(answer, [str((p + d) * n // 100) for d in (5, 10, 15, 20)], rng),
        "solution": f"({p}/100) × {n} = {answer}.",
    }


def dice_sum(rng):
    target = rng.randint(3, 11)
    count = sum(a + b == target for a in range(1, 7) for b in range(1, 7))
    answer = str(Fraction(count, 36))
    wrong = [str(Fraction(c, 36)) for c in range(1, 10) if c != count]
    rng.shuffle(wrong)
    return {
        "topic": "Probability", "kind": "Dice sums",
        "prompt": f"Two fair six-sided dice are rolled. What is P(sum = {target})?",
        "answer": answer, "choices": choices(answer, wrong, rng),
        "solution": f"{count} ordered outcomes have sum {target}, out of 36. P = {count}/36 = {answer}.",
    }


def money(value):
    return f"-${-value}" if value < 0 else f"${value}"


def expected_payoff(rng):
    gain, loss = rng.randint(1, 5), rng.randint(1, 5)
    value = Fraction(12 * gain - 9 * loss, 6)
    answer = money(value)
    return {
        "topic": "Expected value", "kind": "Die payoff",
        "prompt": (f"Roll a fair die and call its face X. Earn ${gain} × X if X is even "
                   f"and lose ${loss} × X if X is odd. What is the expected payoff?"),
        "answer": answer,
        "choices": choices(answer, [money(value + d) for d in (1, -1, 2, -2)], rng),
        "solution": f"E = [{gain}(2 + 4 + 6) − {loss}(1 + 3 + 5)]/6 = {answer}.",
    }


def committee(rng):
    n, k = rng.randint(6, 10), rng.choice([2, 3, 4])
    value = math.comb(n, k)
    answer = str(value)
    wrong = [str(x) for x in (math.perm(n, k), math.comb(n, k-1),
                              math.comb(n+1, k), value+n, max(1, value-n), value+2*n)]
    return {
        "topic": "Combinatorics", "kind": "Committees",
        "prompt": f"How many different committees of {k} can be chosen from {n} people?",
        "answer": answer, "choices": choices(answer, wrong, rng),
        "solution": f"Order does not matter: choose({n}, {k}) = {n}!/({k}!({n}-{k})!) = {answer}.",
    }


def bayes_rule(rng):
    p = rng.choice([20, 25, 30, 40, 50])
    se = rng.choice([60, 75, 80, 90])
    fp = rng.choice([10, 20, 25])
    a, b = p * se, (100-p) * fp
    value = Fraction(a, a+b)
    answer = str(value)
    wrong = [str(x) for x in (Fraction(a, 10000), Fraction(a+b, 10000),
                              Fraction(se, 100), Fraction(p, 100),
                              1-value, Fraction(fp, 100))]
    return {
        "topic": "Conditional probability", "kind": "Bayes' rule",
        "prompt": (f"A condition has prevalence {p}%. A test is positive for {se}% of affected "
                   f"people and {fp}% of unaffected people. What is P(affected | positive)?"),
        "answer": answer, "choices": choices(answer, wrong, rng),
        "solution": f"P(affected | positive) = ({p} × {se})/[({p} × {se}) + ({100-p} × {fp})] = {answer}.",
    }


GENERATORS = [percentage, dice_sum, expected_payoff, committee, bayes_rule]


def make_questions(rng=None):
    """Two instances per type in random order, without repeated prompts."""
    rng = rng or random.Random()
    generators = GENERATORS * 2
    rng.shuffle(generators)
    questions, seen = [], set()
    for generator in generators:
        for _ in range(100):
            question = generator(rng)
            if question["prompt"] not in seen:
                break
        else:
            raise RuntimeError("Could not generate a distinct question")
        questions.append(question)
        seen.add(question["prompt"])
    return questions
