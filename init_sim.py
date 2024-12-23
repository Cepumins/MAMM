import math

tax = 0.00

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
        bid = (balances[0] - (invariant / math.prod([b ** w for b, w in zip(new_balances[1:], weights[1:])])) ** (-1 / (sum(weights) - weights[0] - 1))) / (1 + tax)

        # Calculate ask price
        new_balances[i] -= 2  # Subtract two units from the current asset to return to original and then 1 less
        ask = ((invariant / math.prod([b ** w for b, w in zip(new_balances[1:], weights[1:])])) ** (-1 / (sum(weights) - weights[0] - 1)) - balances[0]) * (1 + tax)

        # Print bid/ask information
        print(f"{names[i]} Bid Price (in {names[0]}): {bid:.4f}")
        print(f"{names[i]} Ask Price (in {names[0]}): {ask:.4f}")

def calculate_invariant(balances, weights):
    invariant = 1
    for balance, weight in zip(balances, weights):
        invariant *= balance ** weight
    return invariant

def calculate_from_values_and_spots(values, spots):
    total_value = sum(values)
    weights = [value / total_value for value in values]
    balances = [value / spot for value, spot in zip(values, spots)]
    invariant = calculate_invariant(balances, weights)
    return lp_asset_names, weights, spots, values, balances, invariant

def calculate_from_values_and_balances(values, balances):
    total_value = sum(values)
    weights = [value / total_value for value in values]
    spots = [value / balance for value, balance in zip(values, balances)]
    invariant = calculate_invariant(balances, weights)
    return lp_asset_names, weights, spots, values, balances, invariant

def calculate_from_total_weights_and_spots(total, weights, spots):
    values = [total * weight for weight in weights]
    balances = [value / spot for value, spot in zip(values, spots)]
    invariant = calculate_invariant(balances, weights)
    return lp_asset_names, weights, spots, values, balances, invariant

def calculate_from_balances_and_weights(balances, weights):
    spots = [(balances[0] / weights[0]) / (balance / weight) for balance, weight in zip(balances[0:], weights)]
    values = [balance * spot for balance, spot in zip(balances, spots)]
    total_value = sum(values)
    invariant = calculate_invariant(balances, weights)
    return lp_asset_names, weights, spots, values, balances, invariant

def calculate_from_balances_and_spots(balances, spots):
    values = [balance * spot for balance, spot in zip(balances, spots)]
    total_value = sum(values)
    weights = [value / total_value for value in values]
    invariant = calculate_invariant(balances, weights)
    return lp_asset_names, weights, spots, values, balances, invariant

def initialize_pool():
    def get_user_choice():
        print("How would you like to initialize the pool? Choose an option:")
        print("1) Values and Spots")
        print("2) Values and Balances")
        print("3) Total, Weights, and Spots")
        print("4) Balances and Weights")
        print("5) Balances and Spots")
        while True:
            try:
                choice = int(input("Enter the number of your choice (1-5): "))
                if 1 <= choice <= 5:
                    return choice
                else:
                    print("Please enter a valid option (1-5).")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")

    def get_asset_names():
        while True:
            names = input("Enter asset names separated by commas (e.g., usd, eur, y, x): ").strip().upper().split(',')
            # Remove leading/trailing whitespace from each name
            names = [name.strip() for name in names if name.strip()]  # Filter out empty strings
            if len(names) < 2:
                print("Please enter at least two asset names.")
            else:
                return names

    def get_values(names):
        values = []
        for name in names:
            value = float(input(f"Enter the value for {name}: "))
            values.append(value)
        return values

    def get_spots(names):
        spots = [1] # Spot price for the first asset is always 1
        for name in names[1:]:
            spot = float(input(f"Enter the spot price for {name}: "))
            spots.append(spot)
        return spots

    def get_balances(names):
        balances = []
        for name in names:
            balance = float(input(f"Enter the balance for {name}: "))
            balances.append(balance)
        return balances

    def get_weights(names):
        while True:
            weights = []
            for name in names[1:]:
                weight = float(input(f"Enter the weight for {name} (as a decimal, e.g., 0.3): "))
                weights.append(weight)
            first_weight = 1 - sum(weights)
            if first_weight > 0:
                weights.insert(0, first_weight)  # Add the first asset's weight at the beginning of the list
                return weights
            else:
                print("The first asset's weight must be positive. Please enter the weights again.")

    def get_total():
        return float(input("Enter the total value of the pool: "))

    choice = get_user_choice()
    global lp_asset_names
    lp_asset_names = get_asset_names()

    if choice == 1:
        print("You chose to initialize the pool with Values and Spots.")
        values = get_values(lp_asset_names)
        spots = get_spots(lp_asset_names)
        return calculate_from_values_and_spots(values, spots)

    elif choice == 2:
        print("You chose to initialize the pool with Values and Balances.")
        values = get_values(lp_asset_names)
        balances = get_balances(lp_asset_names)
        return calculate_from_values_and_balances(values, balances)

    elif choice == 3:
        print("You chose to initialize the pool with Total, Weights, and Spots.")
        total = get_total()
        weights = get_weights(lp_asset_names)
        spots = get_spots(lp_asset_names)
        return calculate_from_total_weights_and_spots(total, weights, spots)

    elif choice == 4:
        print("You chose to initialize the pool with Balances and Weights.")
        balances = get_balances(lp_asset_names)
        weights = get_weights(lp_asset_names)
        return calculate_from_balances_and_weights(balances, weights)

    elif choice == 5:
        print("You chose to initialize the pool with Balances and Spots.")
        balances = get_balances(lp_asset_names)
        spots = get_spots(lp_asset_names)
        return calculate_from_balances_and_spots(balances, spots)

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
        asset = input(prompt).strip().upper()
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

        # Print updated pool balances
        show_pool_info(*calculate_from_balances_and_weights(lp_asset_balances, lp_asset_weights))

# Initialize the pool
pool_data = initialize_pool()
lp_asset_names, lp_asset_weights, lp_asset_spots, lp_asset_values, lp_asset_balances, initial_invariant = pool_data

# Show the initial pool state
show_pool_info(lp_asset_names, lp_asset_weights, lp_asset_spots, lp_asset_values, lp_asset_balances, initial_invariant)

# Start the trading loop
trading_loop()
