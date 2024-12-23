import math

tax = 0.00

# Initial pool setup
#lp_asset_names = ["usd", "eur", "aapl"]
#lp_asset_weights = [0.4, 0.2, 0.4]
#lp_asset_spots = [1, 1.1, 220]
#lp_asset_total = 5000

lp_asset_names = ["y", "x", "z", "a"]
lp_asset_weights = [0.4, 0.3, 0.2, 0.1]
lp_asset_spots = [1, 1.5, 0.5, 0.25]
lp_asset_total = 5000

# Calculate initial asset values and balances
lp_asset_values = [weight * lp_asset_total for weight in lp_asset_weights]
lp_asset_balances = [value / spot for value, spot in zip(lp_asset_values, lp_asset_spots)]

def show_pool_info(names, weights, spots, values, balances, invariant):
    # Round each element in the lists to 4 decimal places
    rounded_weights = [round(weight, 4) for weight in weights]
    rounded_spots = [round(spot, 4) for spot in spots]
    rounded_values = [round(value, 4) for value in values]
    rounded_balances = [round(balance, 4) for balance in balances]

    # Print the formatted output
    print(f"Asset Names: {names}")
    print(f"Asset Weights: {rounded_weights}")
    print(f"Asset Spots: {rounded_spots}")
    print(f"Asset Values: {rounded_values}")
    print(f"Asset Balances: {rounded_balances}")
    print(f"Pool's Invariant Value: {invariant:.8f}")

    # Calculate and display bid and ask prices for remaining assets
    for i in range(1, len(names)):
        # Calculate bid price
        new_balances = balances.copy()
        new_balances[i] += 1  # Hypothetically add one unit of the current asset
        bid = (balances[0] - (invariant / math.prod([b ** w for b, w in zip(new_balances[1:], weights[1:])])  ) ** (-1 / (sum(weights) - weights[0] - 1))) / (1 + tax)

        """
        # Calculate bid price
        sum_weights_excluding_first = sum(weights) - weights[0]
        numerator = invariant
        denominator = math.prod([b ** w for b, w in zip(new_balances[1:], weights[1:])])  # Exclude first asset's balance and weight
        exponent = -1 / (sum_weights_excluding_first - 1)
        bid_value = (balances[0] - (numerator / denominator) ** exponent) / (1 + tax)

        # Print the formula with actual values
        print(f"Bid Calculation:")
        print(f"bid = ({balances[0]} - ({invariant} / math.prod([{', '.join([f'({b} ** {w})' for b, w in zip(new_balances[1:], weights[1:])])}])) ** ({exponent:.4f}))) / (1 + {tax})")
        print(f"= ({balances[0]} - ({invariant} / {denominator}) ** ({exponent:.4f}))) / (1 + {tax})")
        print(f"= ({balances[0]} - ({numerator} / {denominator}) ** {exponent:.4f}) / (1 + {tax})")
        print(f"= {bid_value:.4f}")"""

        # Calculate ask price
        new_balances[i] -= 2  # Subtract two units from the current asset to return to original and then 1 less
        ask = ((invariant / math.prod([b ** w for b, w in zip(new_balances[1:], weights[1:])]) ) ** (-1 / (sum(weights) - weights[0] - 1)) - balances[0]) * (1 + tax)

        # Print bid/ask information
        print(f"{names[i]} Bid Price (in {names[0]}): {bid:.4f}")
        print(f"{names[i]} Ask Price (in {names[0]}): {ask:.4f}")

# Calculate the initial pool's invariant value
def calculate_invariant(balances, weights):
    invariant = 1
    for balance, weight in zip(balances, weights):
        invariant *= balance ** weight
    return invariant

def calculate_from_balances_and_weights(balances, weights):
    spots = [(balances[0] / weights[0]) / (balance / weight) for balance, weight in zip(balances[0:], weights)]
    values = [balance * spot for balance, spot in zip(balances, spots)]
    total_value = sum(values)
    invariant = calculate_invariant(balances, weights)
    return lp_asset_names, weights, spots, values, balances, invariant

# Function to calculate the new balance of an asset given the invariant
def calculate_new_balance(target_invariant, current_balances, asset_index, weights):
    # All balances except the one we're changing remain the same
    product_of_others = math.prod([b ** w for i, (b, w) in enumerate(zip(current_balances, weights)) if i != asset_index])

    # Use the invariant formula to solve for the new balance
    new_balance = (target_invariant / product_of_others) ** (1 / weights[asset_index])
    return new_balance

def get_valid_action():
    while True:
        action = input("Enter action (buy/sell): ").strip().lower()
        if action in ["buy", "sell"]:
            return action
        else:
            print("Invalid action. Please enter 'buy' or 'sell'.")

def get_valid_asset(prompt, valid_assets):
    while True:
        asset = input(prompt).strip().lower()
        if asset in valid_assets:
            return asset
        else:
            print(f"Invalid asset. Please enter one of the following: {', '.join(valid_assets)}.")

def get_valid_amount():
    while True:
        try:
            amount = float(input("Enter the amount to trade: "))
            if amount > 0:
                return amount
            else:
                print("Amount must be greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def trading_loop():
    while True:
        # Get user input
        # Get user input with validation
        action = get_valid_action()
        asset_to_trade = get_valid_asset(f"Enter the asset to trade ({'/'.join(lp_asset_names)}): ", lp_asset_names)
        trade_amount = get_valid_amount()
        asset_in_return = get_valid_asset(f"Enter the asset in return ({'/'.join(lp_asset_names)}): ", lp_asset_names)

        # Identify indices of assets
        trade_index = lp_asset_names.index(asset_to_trade)
        return_index = lp_asset_names.index(asset_in_return)

        if action == "buy":
            # Decrease the balance of the asset being bought
            lp_asset_balances[trade_index] -= trade_amount

        elif action == "sell":
            # Increase the balance of the asset being sold
            lp_asset_balances[trade_index] += trade_amount

        # Calculate the new balance of the asset being used for the trade
        new_balance = calculate_new_balance(initial_invariant, lp_asset_balances, return_index, lp_asset_weights)

        if action == "buy":
            # Calculate how much of the asset to ask from the user
            amount_received = (new_balance - lp_asset_balances[return_index]) * (1 + tax)

            # Print the result
            print(f"You bought {trade_amount} {asset_to_trade} and need to pay {amount_received:.4f} {asset_in_return}.")

            real_new_balance = lp_asset_balances[return_index] + amount_received
            # Adjust the pool's balance with the new amount
            lp_asset_balances[return_index] = real_new_balance

        elif action == "sell":
            # Calculate how much of the asset to ask from the user
            amount_given = (lp_asset_balances[return_index] - new_balance) / (1 + tax)

            # Print the result
            print(f"You sold {trade_amount} {asset_to_trade} and received {amount_given:.4f} {asset_in_return}.")

            real_new_balance = lp_asset_balances[return_index] - amount_given
            # Adjust the pool's balance with the new amount
            lp_asset_balances[return_index] = real_new_balance

        # calculate the new inv
        #new_invariant = calculate_invariant(lp_asset_balances, lp_asset_weights)

        # Print updated pool balances
        #show_pool_info(lp_asset_names, lp_asset_weights, lp_asset_balances, new_invariant)
        show_pool_info(*calculate_from_balances_and_weights(lp_asset_balances, lp_asset_weights))
        #print(f"Updated Pool Balances: {lp_asset_balances}")

# Start interactive loop
def main():
    trading_loop()

initial_invariant = calculate_invariant(lp_asset_balances, lp_asset_weights)
show_pool_info(lp_asset_names, lp_asset_weights, lp_asset_spots, lp_asset_values, lp_asset_balances, initial_invariant)

main()
