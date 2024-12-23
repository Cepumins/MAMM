# Predefined asset names
#lp_asset_names = ["usd", "eur", "aapl", "nvda"]


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
    print(f"Pool's Invariant Value: {invariant:.4f}")

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
    #total_weight = sum(weights)
    #first_weight = 1 - total_weight
    #spots = [1.00]  # First asset's spot price is always 1.00
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

def calculate_invariant(balances, weights):
    invariant = 1
    for balance, weight in zip(balances, weights):
        invariant *= balance ** weight
    return invariant

def demo():
    print("pool 1 (from values and spots)")
    show_pool_info(*calculate_from_values_and_spots([50, 37.5, 25, 12.5], [1, 0.5, 0.25, 1.1]))

    print("pool 2 (from values and balances)")
    show_pool_info(*calculate_from_values_and_balances([50, 37.5, 25, 12.5], [50, 75, 100, 11.3636]))

    print("pool 3 (from total, weights and spots)")
    show_pool_info(*calculate_from_total_weights_and_spots(125, [0.4, 0.3, 0.2, 0.1], [1, 0.5, 0.25, 1.1]))

    print("pool 4 (from balances and weights)")
    show_pool_info(*calculate_from_balances_and_weights([50, 75, 100, 11.3636], [0.4, 0.3, 0.2, 0.1]))

    print("pool 5 (from balances and spots)")
    show_pool_info(*calculate_from_balances_and_spots([50, 75, 100, 11.3636], [1, 0.5, 0.25, 1.1]))


demo()

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
        names = input("Enter asset names separated by commas (e.g., usd, eur, y, x): ").strip().split(',')
        return [name.strip() for name in names]

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
    names = get_asset_names()

    if choice == 1:
        print("You chose to initialize the pool with Values and Spots.")
        values = get_values(names)
        spots = get_spots(names)
        #show_pool_info(*calculate_from_values_and_spots(values, spots))
        return calculate_from_values_and_spots(values, spots)

    elif choice == 2:
        print("You chose to initialize the pool with Values and Balances.")
        values = get_values(names)
        balances = get_balances(names)
        #show_pool_info(*calculate_from_values_and_balances(values, balances))
        return calculate_from_values_and_balances(values, balances)

    elif choice == 3:
        print("You chose to initialize the pool with Total, Weights, and Spots.")
        total = get_total()
        weights = get_weights(names)
        spots = get_spots(names)
        #show_pool_info(*calculate_from_total_weights_and_spots(total, weights, spots))
        return calculate_from_total_weights_and_spots(total, weights, spots)

    elif choice == 4:
        print("You chose to initialize the pool with Balances and Weights.")
        balances = get_balances(names)
        weights = get_weights(names)
        #show_pool_info(*calculate_from_balances_and_weights(balances, weights))
        return calculate_from_balances_and_weights(balances, weights)

    elif choice == 5:
        print("You chose to initialize the pool with Balances and Spots.")
        balances = get_balances(names)
        spots = get_spots(names)
        #show_pool_info(*calculate_from_balances_and_spots(balances, spots))
        return calculate_from_balances_and_spots(balances, spots)

#show_pool_info(*initialize_pool())
pool_data = initialize_pool()
show_pool_info(*pool_data)
