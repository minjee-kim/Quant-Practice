"""Daily screen topics. The spoken card, then a short drill in the app."""

TOPICS = [
    {
        "key": "conditional",
        "title": "Conditional probability",
        "category": "Probability",
        "say": "P(A|B) = P(A and B) / P(B). Independence is that equality with P(A). Conditional independence is the same equality inside a stratum. Two tests can be dependent in the population and independent given disease.",
        "trap": "Sensitivity is P(positive|disease). It is not P(disease|positive). Say the base rate first.",
    },
    {
        "key": "decision",
        "title": "Expectation with a decision",
        "category": "Expected value",
        "say": "Linearity does not need independence. A decision is an action and a loss: treat or not, test or not, chosen where the two expected losses cross. The value of a test is the drop in expected loss, net of its cost.",
        "trap": "A rule that uses the estimate and ignores the loss. A false positive and a false negative are different actions.",
    },
    {
        "key": "bayes",
        "title": "Bayes",
        "category": "Probability",
        "say": "Posterior is proportional to likelihood times prior. Posterior odds equal prior odds times the likelihood ratio. Beta(a, b) and s successes in n trials gives Beta(a+s, b+n-s). A flat prior is still a prior.",
        "trap": "Calling the posterior probability a p-value, or saying a flat prior is no assumption.",
    },
    {
        "key": "bias",
        "title": "Bias and variance",
        "category": "Regression",
        "say": "MSE = bias squared + variance. Unbiased is not the goal. A confidence interval is a procedure with a coverage rate, not the probability the parameter sits in the interval you just computed.",
        "trap": "Equating low bias with a good answer, or calling a posterior interval a confidence interval.",
    },
    {
        "key": "ols",
        "title": "OLS assumptions",
        "category": "Regression",
        "say": "Consistency needs a linear mean, errors mean zero given X, and no perfect collinearity. Homoskedasticity and uncorrelated errors buy the usual standard errors, not consistency. Normality is only for exact finite-sample t tests.",
        "trap": "Listing normality, independence, and homoskedasticity as if all three were conditions for the coefficient itself.",
    },
    {
        "key": "linear-algebra",
        "title": "Linear algebra",
        "category": "Linear algebra",
        "say": "Ax is rows dotted with x. Unique least squares needs full column rank. The residual is orthogonal to every column of X. Rank-nullity: columns = rank + dimension of the null space.",
        "trap": "Treating a zero determinant, a repeated column, and heteroskedasticity as the same failure. They are not.",
    },
    {
        "key": "distributions",
        "title": "Distributions",
        "category": "Distributions",
        "say": "Name the mean and variance before the probability. Binomial counts successes. Poisson mean equals variance. An exponential clock is memoryless. A sum of independent normals is normal, and the variances add.",
        "trap": "Using the marginal when the question is conditional, or multiplying probabilities that are not independent.",
    },
    {
        "key": "python",
        "title": "Python",
        "category": "Python",
        "say": "A slice stops before the end. // floors, / does not. append changes the list and returns None. b = a does not copy.",
        "trap": "Reading range(n) as 1 through n, or expecting append to return the list.",
    },
]


def topic_for(ordinal):
    return TOPICS[ordinal % len(TOPICS)]
