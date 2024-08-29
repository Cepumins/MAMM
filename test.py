import scipy.optimize as opt
from sympy import symbols, sqrt, lambdify
import sympy as sp

# Define the equation to solve
def equation(x):
    return (x * 0.0347 / 12) - 6 - (x * 0.0302 / 12)

# Use scipy's fsolve to find the root of the equation
solution = opt.fsolve(equation, 30000)  # Initial guess is 0

print(f"The solution for x is: {solution[0]}")



# Define the symbols
x, y, a, b = sp.symbols('x, y, a, b')

# Expression for inv
#inv = x**a * y**(1 - a)

# Define the equation after substituting inv
#equation = sp.Eq((inv / (x - 1)**a)**(1 / (1 - a)) - ask, y)
equation = sp.Eq((x*a / 12), (x * b / 12) + y)

# Solve the equation for 'a'

formula_y = sp.solve(equation, x)

# Display the solutionš
print("Formula for y:")
for sol in formula_y:
    print(sol)
