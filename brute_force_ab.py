from math import log
import numpy as np
from scipy.optimize import minimize
from sympy import symbols, sqrt, lambdify
import sympy as sp


# Define the symbols
x, y, a = symbols('x y a')

# Substitute numerical values for a, b, bid, and ask
numerical_values = {
    x: 1000,  # Example value for a
    y: 50,  # Example value for b
    'bid': 0.024981265611345,  # Example value for bid
    'ask': 0.025018765638663   # Example value for ask
}

# Define the symbols
#a, x, y, ask = sp.symbols('a x y ask')
p0, x0, y0, p1, x1, y1, i, dx, k, t, beta, r, dy, gx = sp.symbols('p1, x0, y0, p1, x1, y1, i, dx, k, t, beta, r, dy, gx')

# Expression for inv
#inv = x**a * y**(1 - a)
p0 = y0 / x0
p1 = y1 / x1
i = k * t ** beta
#r = i * (- dx)
gx = dx / x0
r = k * (abs(gx)) ** beta
dy = y1 - y0


# Define the equation after substituting inv
#equation = sp.Eq((inv / (x - 1)**a)**(1 / (1 - a)) - ask, y)
equation = sp.Eq(p0 * (1 + r) ** (-1), p1)

# Solve the equation for 'a'

formula_a = sp.solve(equation, y1)

# Display the solution
print("Formula for y1:")
for sol in formula_a:
    print(sol)

# Evaluate the formula with the numerical values
a_value = [sol.subs(numerical_values).evalf() for sol in formula_a]

avaialble_weight = 0.6
a_weight = 0

# Display the calculated value of 'a'
for val in a_value:
    a_weight = val
    print(f"\nCalculated weight for a: {a_weight * 100}%")

a_value = avaialble_weight * a_weight
print(f"a value: {a_value}")
b = avaialble_weight - a_value
print(f"b value: {b}")
