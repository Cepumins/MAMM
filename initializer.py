# Predefined asset names
lp_asset_names = ["y", "x", "z"]


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

def main():
    print("pool 1 (from values and spots)")
    show_pool_info(*calculate_from_values_and_spots([50, 50, 25], [1, 0.5, 0.25]))

    print("pool 2 (from values and balances)")
    show_pool_info(*calculate_from_values_and_balances([50, 50, 25], [50, 100, 100]))

    print("pool 3 (from total, weights and spots)")
    show_pool_info(*calculate_from_total_weights_and_spots(125, [0.4, 0.4, 0.2], [1, 0.5, 0.25]))

    print("pool 4 (from balances and weights)")
    show_pool_info(*calculate_from_balances_and_weights([50, 100, 100], [0.4, 0.4, 0.2]))

    print("pool 5 (from balances and spots)")
    show_pool_info(*calculate_from_balances_and_spots([50, 100, 100], [1, 0.5, 0.25]))


main()
