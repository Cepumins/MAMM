import numpy as np
from scipy.optimize import fsolve
from sympy import symbols, Eq, sqrt

# Define the symbols
x, a, b, ask, bid = symbols('x a b ask bid')

# Substitute numerical values for a, b, bid, and ask
numerical_values = {
    a: 0.5,  # Example value for a
    b: 0.5,  # Example value for b
    bid: 0.4950495049504937,  # Example value for bid
    ask: 0.5050505050505123   # Example value for ask
}

# Define the expression for geom_spot
geom_spot = sqrt(bid * ask).subs(numerical_values)

# Print the geom_spot value
print(f"Geometric Spot Value: {geom_spot.evalf()}")

# Define the expression for inv
inv = x**a * (geom_spot * x)**b
#inv = x**a * (0.5 * x)**b

# Define the equation
equation = bid + ask + (inv / (x + 1)**a)**(1/b) - (inv / (x - 1)**a)**(1/b)

# Substitute inv in the equation
equation_substituted = equation.subs('inv', inv)

print(f"equation: {equation_substituted}")


equation_numeric = equation_substituted.subs(numerical_values)

# Convert the equation to a function of x
def equation_to_solve(x_val):
    # Ensure x_val is a scalar, even if fsolve passes it as an array
    x_val_scalar = x_val[0] if isinstance(x_val, np.ndarray) else x_val
    return equation_numeric.subs(x, x_val_scalar).evalf()

# Use fsolve to find the root, which is the solution for x
initial_guess = 2.0  # You can choose an initial guess based on your expectations
solution = fsolve(equation_to_solve, initial_guess)

# Print the solution for x
x = solution[0]
print(f"Solution for x: {x}")

y = x * geom_spot
print(f"Solution for y: {y}")

new_inv = ((y ** b) * (x ** a)).subs(numerical_values)
print(f"New Invariant: {new_inv}")

bid = (y - (new_inv / (x + 1) ** a) ** (1 / b)).subs(numerical_values)
ask = ((new_inv / (x - 1) ** a) ** (1 / b) - y).subs(numerical_values)

print(f"Calculated Bid Price: {bid}")
print(f"Calculated Ask Price: {ask}")
