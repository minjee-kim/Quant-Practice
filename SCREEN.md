# Screen list

Probability and regression, out loud, not from notes. The app is the drill. This page is the sentence to say before you start.

**[Open today's set](https://quant-practice.streamlit.app/)**

Five questions, one topic, then stop. The topic changes with the day. A mixed set of 10 is there when you want it.

## Say these

**Conditional probability.** \(P(A\mid B)=P(A\cap B)/P(B)\). Independence is that equality with \(P(A)\). Conditional independence is the same equality inside a stratum. Sensitivity is not \(P(\text{disease}\mid\text{positive})\).

**Expectation with a decision.** Linearity does not need independence. Choose the action with the smaller expected loss. The value of a test is the drop in expected loss, net of its cost.

**Bayes.** Posterior odds = prior odds times the likelihood ratio. \(\mathrm{Beta}(a,b)\) and \(s\) successes in \(n\) trials gives \(\mathrm{Beta}(a+s, b+n-s)\). A flat prior is still a prior.

**Bias and variance.** \(\mathrm{MSE}=\mathrm{bias}^2+\mathrm{variance}\). A confidence interval is a coverage rate of a procedure, not the probability the parameter is in the interval you just computed.

**OLS.** Consistency needs a linear mean, errors mean zero given \(X\), and no perfect collinearity. Heteroskedasticity and clustering break the default standard errors, not consistency. An omitted factor correlated with \(X\) is absorbed into the coefficient. Classical measurement error in \(X\) attenuates. Near collinearity inflates variance.

## Also in the app

Linear algebra: \(Ax\), determinant, rank, eigenvalues of a diagonal matrix, full column rank, residual orthogonal to the columns. The picture, if you want it, is the Essence of Linear Algebra series. The drill is the app.

Distributions: uniform, normal, binomial, geometric, Poisson, exponential.

Python: slice, `//` versus `/`, `append` returns `None`, `range` stops before the end, two names for one list.
