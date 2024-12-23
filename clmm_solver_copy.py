from math import log
from sympy import symbols, sqrt, solve, Eq
import sympy as sp

# Define the symbols
#a, x, y, ask = sp.symbols('a x y ask')
#x, y, wx, wy, L, Pn, Px, value, p_coeff, mult, K, dy, p = sp.symbols('x, y, wx, wy, L, Pn, Px, value, p_coeff, mult, K, dy, p')
x0, p0, x1, p1, p_coeff, L, Pn, Px, y0, y1, value1, valueHold, m = sp.symbols('x0, p0, x1, p1, p_coeff, L, Pn, Px, y0, y1, value1, valueHold, m', positive = True)
loss, dy = symbols("loss, dy")
#L = (-sqrt(Pn)*sqrt(Px)*x - y - sqrt(-2*sqrt(Pn)*sqrt(Px)*x*y + Pn*Px*x**2 + 4*Px*x*y + y**2))/(2*(sqrt(Pn) - sqrt(Px)))
# x = L*(-sqrt(Pn)*sqrt(Px) - p + sqrt(-2*sqrt(Pn)*sqrt(Px)*p + Pn*Px + 4*Px*p + p**2))/(2*sqrt(Px)*p)
# y = p * x

# Expression for inv
#inv = x**a * y**(1 - a)
#PV = C * (1 / r - 1 / (r * (1 + r)**t)) + FV / (1 + r)**t
#a = b * c
#p = y / x
#p0 = y0 / x0
#p1 = y1 / x1
y0 = p0 * x0
#p1 = p0 * m
#valueLP = y + p * x
Pn = p0 / p_coeff
Px = p0 * p_coeff
L = sqrt(p0)*x0*(sqrt(p_coeff) + p_coeff)/(p_coeff - 1)
#x0 = L*(p0 + sqrt(p0/p_coeff)*sqrt(p0*p_coeff) + sqrt(2)*sqrt(p0*(2*p0*p_coeff + p0 - sqrt(p0/p_coeff)*sqrt(p0*p_coeff))))/(2*(-sqrt(p0/p_coeff) + sqrt(p0*p_coeff)))

#y0 = p0 * x0
#L = (x0 + L/sqrt(Px)) * (y0 + L * sqrt(Pn))
#L = (x1 + L/sqrt(Px)) * (y1 + L * sqrt(Pn))
#L = x0*(p0 + sqrt(p0/p_coeff)*sqrt(p0*p_coeff) + sqrt(2)*sqrt(p0*(2*p0*p_coeff + p0 - sqrt(p0/p_coeff)*sqrt(p0*p_coeff))))/(2*(-sqrt(p0/p_coeff) + sqrt(p0*p_coeff)))
#x1 = L*(-sqrt(Pn)*sqrt(Px) - p1 + sqrt(-2*sqrt(Pn)*sqrt(Px)*p1 + Pn*Px + 4*Px*p1 + p1**2))/(2*sqrt(Px)*p1)
#y1 = L*(-sqrt(Pn)*sqrt(Px) - p1 + sqrt(-2*sqrt(Pn)*sqrt(Px)*p1 + Pn*Px + 4*Px*p1 + p1**2))/(2*sqrt(Px))
#y1 = x1 * p1
#value1 = y1 * 2
#valueHold = y0 + x0 * p1


#K = (x0 + L / sqrt(Px)) * (y0 + L * sqrt(Pn))
#L = sqrt(K)

#L > 0
#K = (x0 + L/sqrt(Px)) * (y0 + L * sqrt(Pn))
#K = (x + L/sqrt(Px)) * (y + L * sqrt(Pn))
#inv = x**wx * y**wy
#inv = x**wx * y**wy
#new_y = (inv**(1/wx)*px*p_mult*wx/wy)**(wx/(wx+wy))

#L = x0*(p0 + sqrt(p0/p_coeff)*sqrt(p0*p_coeff) + sqrt(2)*sqrt(p0*(2*p0*p_coeff + p0 - sqrt(p0/p_coeff)*sqrt(p0*p_coeff))))/(2*(-sqrt(p0/p_coeff) + sqrt(p0*p_coeff)))


#K = L ** 2
# Define the equation after substituting inv
#equation = sp.Eq((inv / (x - 1)**a)**(1 / (1 - a)) - ask, y)
#equation = sp.Eq((x0 + L/sqrt(Px)) * (y0 + L * sqrt(Pn)), K)
equation = sp.Eq(
    #L*(-sqrt(Pn)*sqrt(Px) - p1 + sqrt(-2*sqrt(Pn)*sqrt(Px)*p1 + Pn*Px + 4*Px*p1 + p1**2))/(2*sqrt(Px)*p1)
    #(x0 - 1 + L / sqrt(Px)) * (y0 + dy + L * sqrt(Pn))
    (x0 + L/sqrt(Px)) * (y0 + L * sqrt(Pn))
    ,
    L ** 2
    #x0*(-sqrt(Pn)*sqrt(Px) - p0 - sqrt(-2*sqrt(Pn)*sqrt(Px)*p0 + Pn*Px + 4*Px*p0 + p0**2))/(2*(sqrt(Pn) - sqrt(Px)))
)

# Solve the equation for 'a'

formula_mult = sp.solve(equation, y0)

# Display the solution
print("Formula for mult:")
for sol in formula_mult:
    print(sol)

# Substitute numerical values for a, b, bid, and ask
numerical_values = {
    x0: 5,  # Example value for a
    #y0: 15,  # Example value for b
    p0: 3,
    p_coeff: 3,
    #m: 2
    #L: 20.4903810567666,
    #p1: 6,
    #Pn: 1,
    #Px: 9
}

# if p*coef only defined, then the price interval changes with price change
# we use fixed price range, so that the Pn and Px must remain constant

numerical_solutions = [sol.subs(numerical_values) for sol in formula_mult]

# Display the results
print("Numerical solutions for L:")
for sol in numerical_solutions:
    print(sol.evalf())  # Evaluate to get a floating-point number
