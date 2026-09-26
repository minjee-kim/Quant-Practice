"""Parameterized variants of published Jane Street interview-preparation problems.

Source: Jane Street, Probability & Markets (official trading/research guide).
These are adaptations for multiple-choice practice, not claims about live interviews.
"""

import math
import random
from fractions import Fraction

GUIDE_URL = "https://www.janestreet.com/static/pdfs/trading-interview.pdf"


def choices(answer, wrong, rng):
    """Make four distinct labels; never silently accept a broken generator."""
    options = [answer]
    for value in wrong:
        if value not in options:
            options.append(value)
        if len(options) == 4:
            break
    if len(options) != 4:
        raise ValueError("Need three distinct wrong answers")
    rng.shuffle(options)
    return options


def problem(topic, kind, prompt, answer, wrong, solution, page, rng):
    """Package a problem with its official guide page and worked answer."""
    answer = str(answer)
    return {
        "topic": topic,
        "kind": kind,
        "prompt": prompt,
        "answer": answer,
        "choices": choices(answer, [str(value) for value in wrong], rng),
        "solution": solution,
        "source_name": f"Jane Street, Probability & Markets, p. {page}",
        "source_url": f"{GUIDE_URL}#page={page + 1}",
    }


def dice_sum(rng):
    target = rng.randint(3, 11)
    count = sum(a + b == target for a in range(1, 7) for b in range(1, 7))
    value = Fraction(count, 36)
    return problem(
        "Counting", "Two dice: sum",
        f"A red die and a blue die are rolled. What is P(their sum is {target})?",
        value, [Fraction(1, 11), Fraction(count - 1, 36),
                Fraction(count + 1, 36), Fraction(max(1, count - 2), 36)],
        f"The dice are distinct, giving 36 ordered outcomes. {count} pairs sum to "
        f"{target}, so P = {count}/36 = {value}.",
        2, rng,
    )


def card_draws(rng):
    label, count = rng.choice([
        ("clubs", 13), ("face cards", 12), ("aces", 4), ("red cards", 26)
    ])
    replace = rng.choice([True, False])
    first = Fraction(count, 52)
    with_replacement = first * first
    without_replacement = first * Fraction(count - 1, 51)
    value = with_replacement if replace else without_replacement
    condition = "replacing the first card" if replace else "without replacing the first card"
    return problem(
        "Probability", "Card draws",
        f"Draw two cards from a standard 52-card deck, {condition}. "
        f"What is P(both are {label})?",
        value, [without_replacement if replace else with_replacement,
                first, Fraction(count - 1, 51),
                first * Fraction(count - 1, 52), first * Fraction(count, 51)],
        f"The first success has probability {count}/52. "
        + (f"Replacement leaves {count}/52 for the second draw."
           if replace else f"Without replacement, the second chance is {count - 1}/51.")
        + f" Multiply to get {value}.",
        4, rng,
    )


def odd_product(rng):
    rolls = rng.randint(2, 5)
    value = Fraction(1, 2) ** rolls
    return problem(
        "Independence", "Odd die product",
        f"Roll a fair six-sided die {rolls} times. What is P(the product is odd)?",
        value, [Fraction(1, 2) ** (rolls - 1), Fraction(1, 2) ** (rolls + 1),
                Fraction(1, 3) ** rolls, Fraction(1, 2)],
        f"The product is odd only when all {rolls} rolls are odd. "
        f"Independence gives (3/6)^{rolls} = {value}.",
        4, rng,
    )


def weighted_die(rng):
    sides = rng.choice([6, 8, 10])
    heavy = rng.choice([Fraction(1, 3), Fraction(1, 2), Fraction(2, 3)])
    other_mean = Fraction(sides, 2)
    value = heavy * sides + (1 - heavy) * other_mean
    return problem(
        "Expected value", "Weighted die",
        f"A {sides}-sided die lands on {sides} with probability {heavy}; "
        "the other faces are equally likely. What is E[X]?",
        value, [Fraction(sides + 1, 2), heavy * sides, other_mean,
                value - Fraction(1, 2), value + Fraction(1, 2)],
        f"The other faces 1 through {sides - 1} average {other_mean}. "
        f"Thus E[X] = ({heavy})({sides}) + (1 - {heavy})({other_mean}) = {value}.",
        5, rng,
    )


def conditional_die_mean(rng):
    sides = rng.choice([6, 8, 10])
    minimum = rng.randint(2, sides - 2)
    value = Fraction(minimum + sides, 2)
    return problem(
        "Conditional expectation", "Die above a threshold",
        f"X is a fair {sides}-sided die roll. What is E[X | X is at least {minimum}]?",
        value, [Fraction(sides + 1, 2), minimum, sides,
                Fraction(minimum + sides - 1, 2),
                Fraction(minimum + sides + 1, 2)],
        f"Given the condition, {minimum}, {minimum + 1}, ..., {sides} are "
        f"equally likely. Their mean is ({minimum} + {sides})/2 = {value}.",
        7, rng,
    )


def conditional_coins(rng):
    flips = rng.randint(3, 6)
    heads = rng.randint(1, flips - 1)
    ways = math.comb(flips, heads)
    value = Fraction(ways, 2 ** flips - 1)
    return problem(
        "Conditional probability", "Heads given a tail",
        f"Flip {flips} fair coins. Given at least one tail, what is "
        f"P(exactly {heads} heads)?",
        value, [Fraction(ways, 2 ** flips),
                Fraction(ways, 2 ** flips - 2),
                Fraction(ways - 1, 2 ** flips - 1),
                1 - value, Fraction(heads, flips)],
        f"Of the 2^{flips} equally likely sequences, exclude all heads. "
        f"Exactly {heads} heads occurs in C({flips},{heads}) = {ways} "
        f"sequences, so P = {ways}/(2^{flips} - 1) = {value}.",
        7, rng,
    )


def max_dice(rng):
    sides = rng.choice([4, 6, 8])
    rolls = rng.choice([2, 3])
    value = sum((1 - Fraction(j, sides) ** rolls for j in range(sides)),
                Fraction(0))
    return problem(
        "Expected value", "Maximum of dice",
        f"Roll {rolls} independent fair {sides}-sided dice. "
        "What is the expected maximum?",
        value, [Fraction(sides + 1, 2), value - Fraction(1, 2),
                value + Fraction(1, 2), sides, value - 1],
        f"For M = max, P(M > j) = 1 - (j/{sides})^{rolls}. "
        f"Sum this over j = 0,...,{sides - 1} to get E[M] = {value}.",
        10, rng,
    )


def optimal_reroll(rng):
    sides = rng.choice([4, 6, 8, 10])
    new_roll_mean = Fraction(sides + 1, 2)
    value = sum((max(Fraction(x), new_roll_mean) for x in range(1, sides + 1)),
                Fraction(0)) / sides
    return problem(
        "Decision making", "One optional reroll",
        f"Roll a fair {sides}-sided die. After seeing it, you may keep it or "
        "reroll once and must accept the second result. What is your optimal "
        "expected final value?",
        value, [new_roll_mean, value - Fraction(1, 2),
                value + Fraction(1, 2), value + Fraction(1, 4), sides],
        f"A fresh roll averages {new_roll_mean}; reroll a first result below "
        f"that and keep one above it. Average max(x, {new_roll_mean}) "
        f"over x = 1,...,{sides}: {value}.",
        10, rng,
    )


def heads_in_row(rng):
    streak = rng.randint(2, 4)
    value = 2 ** (streak + 1) - 2
    return problem(
        "Stopping times", "Consecutive heads",
        f"Flip a fair coin until you get {streak} heads in a row. "
        "How many flips do you expect?",
        value, [2 ** streak, 2 ** (streak + 1),
                2 ** (streak + 1) - 1, 2 ** streak + 2],
        f"A run-length recursion gives E_1 = 2 and E_j = 2E_(j-1) + 2. "
        f"Therefore E_{streak} = 2^({streak + 1}) - 2 = {value}.",
        11, rng,
    )


def money(amount):
    return f"-${-amount}" if amount < 0 else f"${amount}"


def die_contract(rng):
    sides = rng.choice([6, 8, 10, 20])
    multiplier = rng.choice([2, 4])
    fair_value = multiplier * (sides + 1) // 2
    cost = fair_value + rng.choice([-4, -2, 0, 2, 4])
    value = fair_value - cost
    return problem(
        "Markets", "Die contract value",
        f"A contract pays ${multiplier} times the face of a fair {sides}-sided "
        f"die. You buy it for ${cost}. What is your expected profit?",
        money(value), [money(value + d) for d in (-4, -2, 2, 4)],
        f"The average face is ({sides} + 1)/2. Expected payout is "
        f"${fair_value}, so expected profit is ${fair_value} - ${cost} = "
        f"{money(value)}.",
        9, rng,
    )


def conditional_prime(rng):
    sides = rng.choice([6, 8, 10, 12])
    primes = [x for x in range(2, sides + 1)
              if all(x % d for d in range(2, math.isqrt(x) + 1))]
    thresholds = [t for t in range(3, sides)
                  if 0 < sum(p <= t for p in primes) < len(primes)]
    threshold = rng.choice(thresholds)
    count = sum(p <= threshold for p in primes)
    total = len(primes)
    value = Fraction(count, total)
    wrong = [Fraction(count, sides), Fraction(count, total + 1),
             Fraction(count, total - 1), 1 - value,
             Fraction(count - 1, total), Fraction(count + 1, total)]
    wrong = [x for x in wrong if 0 <= x <= 1]
    return problem(
        "Conditional probability", "Prime die result",
        f"X is a fair {sides}-sided die roll. Given X is prime, "
        f"what is P(X is at most {threshold})?",
        value, wrong,
        f"The prime faces are {', '.join(map(str, primes))}. "
        f"{count} of these {total} faces are at most {threshold}, "
        f"so the conditional probability is {value}.",
        8, rng,
    )


GENERATORS = [
    dice_sum, card_draws, odd_product, weighted_die, conditional_die_mean,
    conditional_coins, max_dice, optimal_reroll, heads_in_row, die_contract,
    conditional_prime,
]


def make_questions(rng=None):
    """One instance of ten randomly selected, distinct published problem types."""
    rng = rng or random.Random()
    generators = rng.sample(GENERATORS, k=10)
    questions = [generator(rng) for generator in generators]
    if len({q["prompt"] for q in questions}) != 10:
        raise RuntimeError("Duplicate question prompts")
    return questions
