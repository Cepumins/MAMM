import sympy as sp

# Define the symbols
x0, y0, L, p0, p1, p_coeff = sp.symbols('x0 y0 L p0 p1 p_coeff')
m = sp.Symbol('m')  # if 'm' is a variable, ensure it's defined
Px = p0 * p_coeff
Pn = p0 / p_coeff

# Define the components of the equation
y0 = p0 * x0
equation = sp.Eq((x0 + L / sp.sqrt(Px)) * (y0 + L * sp.sqrt(Pn)), L**2)

# Step 1: Display the original equation
print("Step 1: Original equation:")
sp.pprint(equation)

# Step 2: Expand the terms inside the equation
expanded_eq = sp.expand(equation.lhs - equation.rhs)
print("\nStep 2: Expanded equation (lhs - rhs = 0):")
sp.pprint(expanded_eq)

# Step 3: Substitute y0 = p0 * x0 into the equation
substituted_eq = expanded_eq.subs(y0, p0 * x0)
print("\nStep 3: Substitute y0 = p0 * x0:")
sp.pprint(substituted_eq)

# Step 4: Simplify the equation
simplified_eq = sp.simplify(substituted_eq)
print("\nStep 4: Simplified equation:")
sp.pprint(simplified_eq)

# Step 5: Solve for x0
solutions = sp.solve(simplified_eq, x0)
print("\nStep 5: Solutions for x0:")
for sol in solutions:
    sp.pprint(sol)
