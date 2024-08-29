from math import log
import numpy as np
from scipy.optimize import minimize
from sympy import symbols, sqrt, lambdify
import sympy as sp


# Define the symbols
x, y, z, a, b, inv = symbols('x, y, z, a, b, inv')

# Substitute numerical values for a, b, bid, and ask
numerical_values = {
    x: 99,  # Example value for a
    z: 100,
    a: 0.3,
    b: 0.3,
    inv: 75.7858283255199
}

# Define the symbols
x, y, z, a, b, inv = sp.symbols('x, y, z, a, b, inv')

# Expression for inv
#inv = x**a * y**(1 - a)

# Define the equation after substituting inv
#equation = sp.Eq((inv / (x - 1)**a)**(1 / (1 - a)) - ask, y)
equation = sp.Eq((x**a) * (z ** b) * (y ** (1 - a - b)), inv)

# Solve the equation for 'a'

formula_y = sp.solve(equation, y)

# Display the solution
print("Formula for y:")
for sol in formula_y:
    print(sol)

# Evaluate the formula with the numerical values
y_value = [sol.subs(numerical_values).evalf() for sol in formula_y]

for val in y_value:
    a_weight = val
    print(f"\nCalculated y: {val}")
