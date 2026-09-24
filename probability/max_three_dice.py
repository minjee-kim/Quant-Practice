"""
Quant Practice: Maximum of Three Dice

Let X1, X2, X3 be independent rolls of a fair six-sided die.

Define:
    M = max(X1, X2, X3)

Tasks
-----
1. Simulate ONE experiment:
      - roll three dice
      - find their maximum
      - print the three rolls and the maximum

2. Write a function:

      roll_maximum()

   that performs the experiment and returns only the maximum.

3. Run the experiment 100,000 times and estimate:

      E[M]

   using the sample mean.

4. Calculate the theoretical value of E[M] yourself.

   Hint:
      P(M <= k) = P(X1 <= k, X2 <= k, X3 <= k)

   Compare the theoretical answer with your simulation.

5. Estimate the probability distribution of M from your simulation:

      P(M = 1)
      P(M = 2)
      ...
      P(M = 6)

6. Calculate those probabilities theoretically and compare them
   with your simulation.

BONUS
-----
Generalize your code.

Write:

    expected_maximum(n_dice, n_sides, n_simulations)

so that you could estimate, for example:

    maximum of 3 d6
    maximum of 5 d6
    maximum of 3 d20
    maximum of 10 d20

Do not hard-code the possible outcomes.
"""


# ============================================================
# PART 1
# Simulate three d6 rolls and print their maximum
# ============================================================
import random
def roll_three():
    x1 =  random.randint(1, 6)
    x2 =  random.randint(1, 6)
    x3 =  random.randint(1, 6)
    print(x1, x2, x3)
    print(max(x1, x2, x3))

roll_three()



# ============================================================
# PART 2
# Write roll_maximum()
# ============================================================

def roll_maximum():
    x1 =  random.randint(1, 6)
    x2 =  random.randint(1, 6)
    x3 =  random.randint(1, 6)
    return(max(x1, x2, x3))

roll_maximum()


# ============================================================
# PART 3
# Monte Carlo estimate of E[M]
#
# Run roll_maximum() 100,000 times.
# Store the results.
# Calculate their average.
# ============================================================
results = []
for i in range(100000):
    results.append(roll_maximum())

len(results)

# ============================================================
# PART 4
# Theoretical E[M]
#
# Derive this mathematically first.
# Then implement your calculation in Python.
# ============================================================
average = sum(results) / len(results)
print(average)



# ============================================================
# PART 5
# Empirical distribution
#
# Estimate P(M = k) for k = 1,...,6 from your simulations.
# ============================================================




# ============================================================
# PART 6
# Theoretical distribution
#
# Use:
#
# P(M <= k) = (k / 6)^3
#
# Think about how to obtain P(M = k) from this.
# ============================================================




# ============================================================
# BONUS
# ============================================================

def expected_maximum(n_dice, n_sides, n_simulations):
    pass