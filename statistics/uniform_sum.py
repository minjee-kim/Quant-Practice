#########################################################
###  Let X, Y ~ iid Uniform(0,1).
###  Define: Z = X + Y
###  Find the probability density function of Z.
#########################################################

########## Solution ##########
## Because X and Y are independent, 
##  f_Z(z) = ∫ f_X(x) f_Y(z - x) dx
## 
##  Since both X and Y are Uniform(0,1),
##   f_X(x) = 1   for 0 <= x <= 1
##   f_Y(y) = 1   for 0 <= y <= 1
## 
##  Therefore, we only need to determine the range of x for which
##     0 <= x <= 1
##     0 <= z - x <= 1
## 
##  This produces:
##    f_Z(z) = z   for 0 <= z <= 1
##    2 - z        for 1 < z <= 2
##    0            otherwise
###################################

import numpy as np
import matplotlib.pyplot as plt

### 1. PDF of X and Y
def uniform_pdf(x):

    if 0 <= x <= 1:
        return 1

    return 0

### 2. PDF of Z = X + Y
def sum_uniform_pdf(z):

    if 0 <= z <= 1:
        return z

    elif 1 < z <= 2:
        return 2 - z

    else:
        return 0.0

### 3. Plot theoretical PDF
z_values = np.linspace(-0.25, 2.25, 500)

pdf_values = np.array([
    sum_uniform_pdf(z)
    for z in z_values
])

plt.figure(figsize=(8, 5))

plt.plot(
    z_values,
    pdf_values,
    linewidth=2,
    label="Theoretical PDF"
)

plt.xlabel("z")
plt.ylabel("f_Z(z)")
plt.title("Distribution of Z = X + Y")

plt.legend()
plt.grid(alpha=0.3)

plt.show()



### 4. Simulation check 
np.random.seed(123)

n = 100_000

X = np.random.uniform(0, 1, n)
Y = np.random.uniform(0, 1, n)

Z = X + Y


### 5. Compare Simulation with theory 

plt.figure(figsize=(8, 5))

plt.hist(
    Z,
    bins=50,
    density=True,
    alpha=0.4,
    label="Simulation"
)

plt.plot(
    z_values,
    pdf_values,
    linewidth=2,
    label="Theoretical PDF"
)

plt.xlabel("z")
plt.ylabel("Density")
plt.title("X + Y: Simulation vs. Theoretical Distribution")
plt.legend()
plt.grid(alpha=0.3)

plt.show()