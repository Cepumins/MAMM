import math
from scipy.optimize import fsolve

class Pool:
    def __init__(self, balances=None, weights=None, bid=None, ask=None):
        self.balances = balances if balances is not None else [None, None]
        self.bid = bid
        self.ask = ask
        self.weights = weights
        self.invariant = None

        if self.balances[0] is None or self.balances[1] is None:
            if bid is not None and ask is not None and weights is not None:
                self.solve_for_balances()

        if self.weights is None and self.balances[0] is not None and self.balances[1] is not None and bid is not None and ask is not None:
            self.solve_for_weights()

        if self.weights is not None and self.balances[0] is not None and self.balances[1] is not None:
            self.calculate_invariant_and_prices()

    def solve_for_balances(self):
        def equations(vars):
            x, y = vars
            a, b = self.weights
            bid, ask = self.bid, self.ask

            inv = (x**a) * (y**b)

            #eq1 = (x - 1)**a / (x + 1)**a - (y - bid)**b / (y + ask)**b
            eq2 = ask + y - (inv / (x - 1)**a)**(1 / b)
            eq3 = bid - y + (inv / (x + 1)**a)**(1 / b)

            return [eq2, eq3]

        # Initial guess for x and y
        initial_guess = [2, 2]

        # Define constraints for the ratio y/x
        def constraint(vars):
            x, y = vars
            ratio = y / x
            return [(ratio - self.bid), (self.ask - ratio)]

        # Solve for x and y using fsolve
        solution, infodict, ier, mesg = fsolve(equations, initial_guess, full_output=True, xtol=1e-9)

        # Ensure solution is valid and within constraints
        x, y = solution
        if ier != 1 or not (self.bid < y / x < self.ask):
            print("fsolve did not converge or solution did not satisfy constraints:", mesg)
        else:
            self.balances = [x, y]
            self.x, self.y = x, y
            #self.invariant = inv
            print(f"Solved Balances: x = {self.x:.4f}, y = {self.y:.4f}")

    def solve_for_weights(self):
        def equations(vars):
            a, b = vars
            if a + b > 1 or a <= 0 or b <= 0:  # Ensure valid weights
                return [float('inf'), float('inf')]
            inv = self.balances[0]**a * self.balances[1]**b
            eq1 = self.ask - ((inv / (self.balances[0] - 1)**a)**(1/b) - self.balances[1])
            eq2 = self.bid - (self.balances[1] - (inv / (self.balances[0] + 1)**a)**(1/b))
            return [eq1, eq2]

        initial_guess = [0.5, 0.5]  # Start with reasonable weights
        solution, infodict, ier, mesg = fsolve(equations, initial_guess, full_output=True)

        if ier != 1:
            print("fsolve did not converge:", mesg)
        else:
            self.weights = solution
            self.a, self.b = solution
            print(f"Solved Weights: a = {self.a:.4f}, b = {self.b:.4f}")

    def calculate_invariant_and_prices(self):
        x, y = self.balances
        w_x, w_y = self.weights
        self.invariant = (y ** w_y) * (x ** w_x)
        print(f"Invariant: {self.invariant}")

        ask = (self.invariant / (x - 1) ** w_x) ** (1 / w_y) - y
        bid = y - (self.invariant / (x + 1) ** w_x) ** (1 / w_y)

        #print(f"Calculated Ask Price: {ask}")
        #print(f"Calculated Bid Price: {bid}")
        self.ask = ask
        self.bid = bid

    def print_pool_info(self):
        print("Pool info:")
        print(f"Balances: {self.balances}")
        print(f"Weights: {self.weights}")
        print(f"Bid: {self.bid}")
        print(f"Ask: {self.ask}")
        print(f"Invariant: {self.invariant}")
        print(f"")

# Example usage

# Case 1: Known balances and weights, but unknown bid and ask
print("case 1")
balances = [20, 50]
weights = [0.2, 0.4]

pool = Pool(balances=balances, weights=weights)
pool.print_pool_info()

# Case 2: Known bid, ask, and weights, but unknown balances
print("case 2")
weights = [0.3, 0.7]
bid = 0.2127673874378715  # example bid
ask = 0.2158288243561799  # example ask

pool = Pool(weights=weights, bid=bid, ask=ask)
pool.print_pool_info()

# Case 3: Known balances, bid, and ask, but unknown weights
print("case 3")
balances = [100, 50]
bid = 0.2127673874378715  # example bid
ask = 0.2158288243561799  # example ask

pool = Pool(balances=balances, bid=bid, ask=ask)
pool.print_pool_info()
