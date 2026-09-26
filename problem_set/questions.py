"""Parameterized variants of published firm-authored practice examples.

Sources: Jane Street's Probability & Markets guide and Susquehanna's decision
science examples. These are adaptations, not claims about live interviews.
"""

import math
import random
from fractions import Fraction

GUIDE_URL = "https://www.janestreet.com/static/pdfs/trading-interview.pdf"
SIG_SOURCE = (
    "Susquehanna, Game Theory + Decision Science",
    "https://sig.com/who-we-are/game-theory-decision-science/",
)


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


def tex(value):
    """A compact LaTeX integer or exact fraction for displayed math."""
    value = Fraction(value)
    return (str(value.numerator) if value.denominator == 1 else
            rf"\frac{{{value.numerator}}}{{{value.denominator}}}")


def problem(topic, kind, prompt, answer, wrong, solution, page, rng, source=None):
    """Package a problem with its published source and worked answer."""
    answer = str(answer)
    source_name, source_url = source or (
        f"Jane Street, Probability & Markets, p. {page}",
        f"{GUIDE_URL}#page={page + 1}",
    )
    return {
        "topic": topic,
        "kind": kind,
        "prompt": prompt,
        "answer": answer,
        "choices": choices(answer, [str(value) for value in wrong], rng),
        "solution": solution,
        "source_name": source_name,
        "source_url": source_url,
    }


def dice_sum(rng):
    target = rng.randint(3, 11)
    count = sum(a + b == target for a in range(1, 7) for b in range(1, 7))
    value = Fraction(count, 36)
    return problem(
        "Counting", "Two dice: sum",
        f"Roll a fair **red** die and a fair **blue** die. "
        f"What is $P(R+B={target})$, where $R$ and $B$ are their faces?",
        value, [Fraction(1, 11), Fraction(count - 1, 36),
                Fraction(count + 1, 36), Fraction(max(1, count - 2), 36)],
        f"The dice are distinct, giving $6\\times6=36$ ordered outcomes. "
        f"{count} pairs sum to {target}, so "
        f"$P(R+B={target})=\\frac{{{count}}}{{36}}={tex(value)}$.",
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
        f"Draw two cards from a standard 52-card deck, **{condition}**. "
        f"What is $P(\\text{{both are {label}}})$?",
        value, [without_replacement if replace else with_replacement,
                first, Fraction(count - 1, 51),
                first * Fraction(count - 1, 52), first * Fraction(count, 51)],
        f"The first draw succeeds with probability $\\frac{{{count}}}{{52}}$. "
        + (f"With replacement, the second chance is $\\frac{{{count}}}{{52}}$."
           if replace else
           f"Without replacement, it is $\\frac{{{count - 1}}}{{51}}$.")
        + f" Multiply: $P={tex(value)}$.",
        4, rng,
    )


def odd_product(rng):
    rolls = rng.randint(2, 5)
    value = Fraction(1, 2) ** rolls
    return problem(
        "Independence", "Odd die product",
        f"Roll a fair six-sided die {rolls} times. "
        "What is $P(\\text{the product is odd})$?",
        value, [Fraction(1, 2) ** (rolls - 1), Fraction(1, 2) ** (rolls + 1),
                Fraction(1, 3) ** rolls, Fraction(1, 2)],
        f"The product is odd only when all {rolls} rolls are odd. "
        f"Independence gives $P=(\\frac{{3}}{{6}})^{{{rolls}}}={tex(value)}$.",
        4, rng,
    )


def weighted_die(rng):
    sides = rng.choice([6, 8, 10])
    heavy = rng.choice([Fraction(1, 3), Fraction(1, 2), Fraction(2, 3)])
    other_mean = Fraction(sides, 2)
    value = heavy * sides + (1 - heavy) * other_mean
    return problem(
        "Expected value", "Weighted die",
        f"A {sides}-sided die lands on {sides} with probability "
        f"${tex(heavy)}$; the other faces are equally likely. "
        "What is $E[X]$?",
        value, [Fraction(sides + 1, 2), heavy * sides, other_mean,
                value - Fraction(1, 2), value + Fraction(1, 2)],
        f"The other faces $1,\\ldots,{sides - 1}$ average "
        f"${tex(other_mean)}$. Thus "
        f"$E[X]={tex(heavy)}({sides})+"
        f"{tex(1 - heavy)}({tex(other_mean)})={tex(value)}$.",
        5, rng,
    )


def conditional_die_mean(rng):
    sides = rng.choice([6, 8, 10])
    minimum = rng.randint(2, sides - 2)
    value = Fraction(minimum + sides, 2)
    return problem(
        "Conditional expectation", "Die above a threshold",
        f"$X$ is a fair {sides}-sided die roll. "
        f"What is $E[X\\mid X\\ge {minimum}]$?",
        value, [Fraction(sides + 1, 2), minimum, sides,
                Fraction(minimum + sides - 1, 2),
                Fraction(minimum + sides + 1, 2)],
        f"Given the condition, ${minimum},{minimum + 1},\\ldots,{sides}$ "
        f"are equally likely. Their mean is "
        f"$\\frac{{{minimum}+{sides}}}{{2}}={tex(value)}$.",
        7, rng,
    )


def conditional_coins(rng):
    flips = rng.randint(3, 6)
    heads = rng.randint(1, flips - 1)
    ways = math.comb(flips, heads)
    value = Fraction(ways, 2 ** flips - 1)
    return problem(
        "Conditional probability", "Heads given a tail",
        # Use the singular form when the target count is one.
        f"Flip {flips} fair coins. Given **at least one tail**, what is "
        f"$P(\\text{{exactly {heads} {'head' if heads == 1 else 'heads'}}}"
        f"\\mid\\text{{at least one tail}})$?",
        value, [Fraction(ways, 2 ** flips),
                Fraction(ways, 2 ** flips - 2),
                Fraction(ways - 1, 2 ** flips - 1),
                1 - value, Fraction(heads, flips)],
        f"Exclude the all-heads sequence from the $2^{{{flips}}}$ possibilities. "
        f"Exactly {heads} {'head' if heads == 1 else 'heads'} occurs in "
        f"$\\binom{{{flips}}}{{{heads}}}={ways}$ "
        f"sequences, so $P=\\frac{{{ways}}}{{2^{{{flips}}}-1}}={tex(value)}$.",
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
        f"What is $E[\\max(X_1,\\ldots,X_{rolls})]$?",
        value, [Fraction(sides + 1, 2), value - Fraction(1, 2),
                value + Fraction(1, 2), sides, value - 1],
        f"For $M=\\max(X_1,\\ldots,X_{rolls})$, "
        f"$P(M>j)=1-(j/{sides})^{{{rolls}}}$. "
        f"Sum over $j=0,\\ldots,{sides - 1}$ to get $E[M]={tex(value)}$.",
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
        "reroll **once** and must accept the second result. "
        "What is your **optimal expected final value**?",
        value, [new_roll_mean, value - Fraction(1, 2),
                value + Fraction(1, 2), value + Fraction(1, 4), sides],
        f"A fresh roll averages ${tex(new_roll_mean)}$. Reroll a first "
        f"result below that and keep one above it. "
        f"$E[\\text{{final value}}]=\\frac{{1}}{{{sides}}}"
        f"\\sum_{{x=1}}^{{{sides}}}\\max(x,{tex(new_roll_mean)})={tex(value)}$.",
        10, rng,
    )


def heads_in_row(rng):
    streak = rng.randint(2, 4)
    value = 2 ** (streak + 1) - 2
    return problem(
        "Stopping times", "Consecutive heads",
        f"Flip a fair coin until you get {streak} heads in a row. "
        "What is the **expected number of flips**?",
        value, [2 ** streak, 2 ** (streak + 1),
                2 ** (streak + 1) - 1, 2 ** streak + 2],
        f"A run-length recursion gives $E_1=2$ and $E_j=2E_{{j-1}}+2$. "
        f"Therefore $E_{{{streak}}}=2^{{{streak + 1}}}-2={value}$.",
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
        f"Let $X$ be a fair {sides}-sided die roll. A contract pays "
        f"**{multiplier} dollars per point** and costs **{cost} dollars**. "
        f"What is the expected profit $E[{multiplier}X-{cost}]$ in dollars?",
        money(value), [money(value + d) for d in (-4, -2, 2, 4)],
        f"The average face is $E[X]=\\frac{{{sides}+1}}{{2}}$. "
        f"Expected payout is {fair_value} dollars, so "
        f"$E[{multiplier}X-{cost}]={fair_value}-{cost}={value}$ dollars.",
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
        f"$X$ is a fair {sides}-sided die roll. Given that $X$ is prime, "
        f"what is $P(X\\le {threshold}\\mid X\\text{{ is prime}})$?",
        value, wrong,
        f"The prime faces are {', '.join(map(str, primes))}. "
        f"{count} of these {total} faces are at most {threshold}, "
        f"so the conditional probability is $\\frac{{{count}}}{{{total}}}="
        f"{tex(value)}$.",
        8, rng,
    )


def pain_and_rain(rng):
    """Compare conditional rates, adapting Susquehanna's correlation example."""
    rainy_pain, rainy_no_pain, dry_pain, dry_no_pain = rng.choice([
        (14, 7, 6, 2),   # More rainy pain counts, but a lower rainy rate.
        (9, 3, 8, 8),    # Higher rainy rate.
        (8, 8, 3, 3),    # Same rate.
        (4, 8, 9, 9),    # Lower rainy rate.
    ])
    rainy_scale = rng.randint(1, 3)
    dry_scale = rng.randint(1, 3)
    rainy_pain *= rainy_scale
    rainy_no_pain *= rainy_scale
    dry_pain *= dry_scale
    dry_no_pain *= dry_scale
    rainy_rate = Fraction(rainy_pain, rainy_pain + rainy_no_pain)
    dry_rate = Fraction(dry_pain, dry_pain + dry_no_pain)
    answer = ("Rainy days" if rainy_rate > dry_rate else
              "Dry days" if dry_rate > rainy_rate else "Equal in both")
    return problem(
        "Data interpretation", "Pain and rain",
        "Which group has the **higher rate of pain**?\n\n"
        "| Weather | Pain | No pain |\n"
        "|:---|---:|---:|\n"
        f"| Rainy | {rainy_pain} | {rainy_no_pain} |\n"
        f"| Dry | {dry_pain} | {dry_no_pain} |",
        answer, ["Rainy days", "Dry days", "Equal in both", "Cannot tell"],
        f"Compare rates **within** each group: "
        f"$P(\\text{{pain}}\\mid\\text{{rain}})="
        f"\\frac{{{rainy_pain}}}{{{rainy_pain + rainy_no_pain}}}="
        f"{tex(rainy_rate)}$; "
        f"$P(\\text{{pain}}\\mid\\text{{dry}})="
        f"\\frac{{{dry_pain}}}{{{dry_pain + dry_no_pain}}}="
        f"{tex(dry_rate)}$. Answer: **{answer}**.",
        None, rng, source=SIG_SOURCE,
    )


def coin_streak_next_flip(rng):
    streak = rng.randint(3, 10)
    return problem(
        "Independence", "After a heads streak",
        f"A fair coin has just landed heads {streak} times in a row. "
        "What is $P(\\text{heads on the next flip})$?",
        Fraction(1, 2), [Fraction(0), Fraction(1, 4), Fraction(3, 4)],
        "Fair coin flips are independent. A previous streak does not change "
        "the next flip's chance of heads: $P=\\frac{1}{2}$.",
        None, rng, source=SIG_SOURCE,
    )


JANE_STREET_GENERATORS = [
    dice_sum, card_draws, odd_product, weighted_die, conditional_die_mean,
    conditional_coins, max_dice, optimal_reroll, heads_in_row, die_contract,
    conditional_prime,
]
SIG_GENERATORS = [pain_and_rain, coin_streak_next_flip]
GENERATORS = JANE_STREET_GENERATORS + SIG_GENERATORS


def make_questions(rng=None):
    """Ten distinct types, including both Susquehanna examples each round."""
    rng = rng or random.Random()
    generators = rng.sample(JANE_STREET_GENERATORS, k=8) + SIG_GENERATORS[:]
    rng.shuffle(generators)
    questions = [generator(rng) for generator in generators]
    if len({q["prompt"] for q in questions}) != 10:
        raise RuntimeError("Duplicate question prompts")
    return questions
