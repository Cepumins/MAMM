def calculate_ask_bid_prices(p, y):
    # Calculate x amount
    x = y / p

    # Calculate the constant k
    k = x * y

    # Calculate ask price
    #y_new_ask = k / (x - 1)
    #ask = y_new_ask - y

    # Calculate bid price
    #y_new_bid = k / (x + 1)
    #bid = y - y_new_bid
    ask = k / (x - 1) - y
    bid = y - k / (x + 1)

    print(f"A Ask Price: {ask}")
    print(f"A Bid Price: {bid}")

a_v = 50 # USD
a_p = 0.5 # A price

calculate_ask_bid_prices(a_p, a_v)

def calculate_capital_from_bid_ask(bid, ask):
    # Finally, solve for the original y (capital) using k / x
    y = ask * ( (bid + ask) / (ask - bid) - 1)

    print(f"Required USD capital (y): {y}")

a_ask = 2.5  # Example ask price
a_bid = 2 # Example bid price
calculate_capital_from_bid_ask(a_bid, a_ask)

a_y = a_v * a_p

# List of asset names and their corresponding values
names = ["usd", "a", "b"]
assets = [10, a_v, 20]

def calculate_pool_liquidity(asset_list, asset_names):
    total_value = sum(asset_list)
    print(f"Total value of the pool: {total_value}")

    for name, asset in zip(asset_names, asset_list):
        weight = asset / total_value * 100
        print(f"Weight of {name} in the pool: {weight:.2f}%")

# Call the function
calculate_pool_liquidity(assets, names)


weights = [50, 50]
names = ["y", "x"]
liquidity = 1000

def calculate_pool_info(weights, assets, liquidity):
    for weight, asset in zip(weights, assets):
        value = liquidity * weight / 100
        print(f"Value of {asset} in the pool: ${value:.2f}")

    spot_price_y = ( (500 / 50) / (500 / 50) )
    print(spot_price_y)

calculate_pool_info(weights, names, liquidity)
