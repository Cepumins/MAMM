import numpy as np
from scipy.optimize import minimize
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

# Define an initial guess for geom_spot
geom_spot = sqrt(numerical_values[bid] * numerical_values[ask])

# Tolerance for bid/ask matching
tolerance = 1e-10

# Maximum number of iterations to prevent infinite loops
max_iterations = 1

for i in range(max_iterations):
    adjustment_factor = 0.001 / (i + 1)  # Decreasing adjustment factor
    print(f"Iteration {i + 1}: Geometric Spot Value = {geom_spot.evalf()}")

    # Define the expression for inv using the current geom_spot
    inv = x**a * (geom_spot * x)**b

    # Define the equation
    equation = numerical_values[bid] + numerical_values[ask] + \
               (inv / (x + 1)**a)**(1/b) - (inv / (x - 1)**a)**(1/b)

    # Substitute numerical values into the equation
    equation_numeric = equation.subs(numerical_values)

    # Define the function to minimize, i.e., the difference between calculated and actual bid/ask
    def objective_function(x_val):
        x_val_scalar = x_val[0] if isinstance(x_val, np.ndarray) else x_val
        y = x_val_scalar * geom_spot
        print(f"minimizer x: {x_val_scalar}, y: {y}")
        new_inv = ((y ** numerical_values[b]) * (x_val_scalar ** numerical_values[a])).subs(numerical_values)
        calculated_bid = (y - (new_inv / (x_val_scalar + 1) ** numerical_values[a]) ** (1 / numerical_values[b])).subs(numerical_values)
        calculated_ask = ((new_inv / (x_val_scalar - 1) ** numerical_values[a]) ** (1 / numerical_values[b]) - y).subs(numerical_values)
        bid_diff = abs(calculated_bid - numerical_values[bid])
        ask_diff = abs(calculated_ask - numerical_values[ask])
        print(f"diff: {bid_diff + ask_diff}")
        return bid_diff + ask_diff

    # Use minimize to find the best x value
    result = minimize(objective_function, x0=50, method='Nelder-Mead')
    x = result.x[0]

    # Calculate y using the current geom_spot
    y = x * geom_spot

    print(f"x: {x}, y: {y}")

    # Calculate the new invariant
    new_inv = ((y ** numerical_values[b]) * (x ** numerical_values[a])).subs(numerical_values)

    # Calculate the bid and ask based on the current invariant
    calculated_bid = (y - (new_inv / (x + 1) ** numerical_values[a]) ** (1 / numerical_values[b])).subs(numerical_values)
    calculated_ask = ((new_inv / (x - 1) ** numerical_values[a]) ** (1 / numerical_values[b]) - y).subs(numerical_values)

    print(f"bid: {calculated_bid}, ask: {calculated_ask}")

    # Check if the calculated bid/ask are within the tolerance
    if abs(calculated_bid - numerical_values[bid]) < tolerance and abs(calculated_ask - numerical_values[ask]) < tolerance:
        print(f"Converged after {i + 1} iterations")
        break

    # Adjust geom_spot based on the direction of error, with decreasing adjustments
    if calculated_bid > numerical_values[bid] or calculated_ask < numerical_values[ask]:
        geom_spot *= 1 - adjustment_factor  # Decrease geom_spot
        print("decreasing geom")
    else:
        geom_spot *= 1 + adjustment_factor  # Increase geom_spot
        print("increasing geom")

# Print the final results
print(f"Final Geometric Spot Value: {geom_spot.evalf()}")
print(f"Final Solution for x: {x}")
print(f"Final Solution for y: {y}")
print(f"Final Invariant: {new_inv}")
print(f"Final Calculated Bid Price: {calculated_bid}")
print(f"Final Calculated Ask Price: {calculated_ask}")
