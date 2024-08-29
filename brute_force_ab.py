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
a, x, y, ask = sp.symbols('a x y ask')

# Expression for inv
inv = x**a * y**(1 - a)

# Define the equation after substituting inv
equation = sp.Eq((inv / (x - 1)**a)**(1 / (1 - a)) - ask, y)

# Solve the equation for 'a'

formula_a = sp.solve(equation, a)

# Display the solution
print("Formula for a:")
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
