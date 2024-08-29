from math import log
import numpy as np
from scipy.optimize import minimize
from sympy import symbols, sqrt, lambdify

# Define the symbols
x, a, b = symbols('x a b')

# Substitute numerical values for a, b, bid, and ask
numerical_values = {
    a: 0.2,  # Example value for a
    b: 0.4,  # Example value for b
    #'bid': 0.4950495049504937,  # Example value for bid
    #'ask': 0.5050505050505123   # Example value for ask
    'bid': 0.024981265611345,  # Example value for bid
    'ask': 0.025018765638663   # Example value for ask
}

# Define the expression for geom_spot
geom_spot_initial = sqrt(numerical_values['bid'] * numerical_values['ask'])

# Define the expression for inv using symbolic variables
inv_expr = x**a * (x * geom_spot_initial)**b

# Convert the symbolic expression to a numerical function
inv_func = lambdify(x, inv_expr.subs(numerical_values))

# Define the function to minimize
def objective_function(x_val, geom_spot):
    #geom_spot = sqrt(numerical_values['bid'] * numerical_values['ask'])
    #geom_spot = sqrt(current_bid * current_ask)
    y = x_val * geom_spot

    #new_inv = inv_func(x_val)  # Evaluate the invariant numerically
    new_inv = x_val**numerical_values[a] * y**numerical_values[b]

    calculated_bid = y - (new_inv / (x_val + 1) ** numerical_values[a]) ** (1 / numerical_values[b])
    calculated_ask = (new_inv / (x_val - 1) ** numerical_values[a]) ** (1 / numerical_values[b]) - y

    bid_diff = abs(calculated_bid - numerical_values['bid'])
    ask_diff = abs(calculated_ask - numerical_values['ask'])

    # Print for debugging purposes
    print(f"minimizer x: {x_val}, geom_spot: {geom_spot}, y: {y}, diff: {bid_diff + ask_diff}")

    return bid_diff + ask_diff, calculated_bid, calculated_ask

# Wrapper function for minimize
def minimize_wrapper(x_val, geom_spot, current_diff, iteration):
    # Minimize only x while using the current geom_spot
    def objective(x_val_inner):
        diff, calculated_bid, calculated_ask = objective_function(x_val_inner[0], geom_spot)
        return diff

    # Run the minimizer
    #result = minimize(objective, [x_val], method='Nelder-Mead')
    result = minimize(objective, [x_val], method='L-BFGS-B', bounds=[(1e-5, None)])

    # Get the new x value
    x_new = result.x[0]

    # Calculate the new bid and ask using the optimized x
    diff, calculated_bid, calculated_ask = objective_function(x_new, geom_spot)

    # If the difference is smaller, update geom_spot using new bid/ask
    #adjustment_factor = 1 / (iteration + 1)  # Decreasing adjustment factor
    #adjustment_factor = 1 / log(iteration + 2)  # Decreasing adjustment factor
    adjustment_factor = 1
    if diff < current_diff:
        new_geom_spot = geom_spot * (1 - 0.0001 * adjustment_factor)
        print(f"Decreased geom_spot: {new_geom_spot}")
        return x_new, new_geom_spot, diff
    else:
        new_geom_spot = geom_spot * (1 + 0.0001 * adjustment_factor)
        print(f"Increased geom_spot: {new_geom_spot}")
        return x_new, new_geom_spot, diff

# Initial values
initial_x = 10
geom_spot = sqrt(numerical_values['bid'] * numerical_values['ask'])
current_diff = 999999

# Iterate to update geom_spot and x
for i in range(10):  # Limit the number of iterations
    print(f"\nIteration {i + 1}")
    initial_x, geom_spot, current_diff = minimize_wrapper(initial_x, geom_spot, current_diff, i)
    if current_diff < 1e-10:
        break

# Calculate y using the optimized geom_spot
y_opt = initial_x * geom_spot
new_inv = initial_x**numerical_values[a] * y_opt**numerical_values[b]

# Calculate the new invariant
#new_inv = inv_func(x_opt)

# Calculate the final bid and ask based on the optimized invariant
calculated_bid = y_opt - (new_inv / (initial_x + 1) ** numerical_values[a]) ** (1 / numerical_values[b])
calculated_ask = (new_inv / (initial_x - 1) ** numerical_values[a]) ** (1 / numerical_values[b]) - y_opt

# Print the final results
print(f"Final Geometric Spot Value: {geom_spot}")
print(f"Final Solution for x: {initial_x}")
print(f"Final Solution for y: {y_opt}")
print(f"Final Invariant: {new_inv}")
print(f"Final Calculated Bid Price: {calculated_bid}")
print(f"Final Calculated Ask Price: {calculated_ask}")
