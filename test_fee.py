from functools import total_ordering
import pandas as pd

# Load AAPL and MSFT data
aapl_data = pd.read_excel("aapl_10-25-2024_1_min.xlsx")
msft_data = pd.read_excel("msft_25-10-2024_1_min.xlsx")
aapl_data['Time'] = pd.to_datetime(aapl_data['Time'], format="%m/%d/%Y %I:%M:%S %p")
msft_data['Time'] = pd.to_datetime(msft_data['Time'], format="%m/%d/%Y %I:%M:%S %p")

# Merge unique timestamps from both datasets and sort them
unique_times = pd.concat([aapl_data['Time'], msft_data['Time']]).drop_duplicates().sort_values()
#print(unique_times)

# Define assets and initialize parameters
assets = ["USD", "AAPL", "MSFT"]
data = {"AAPL": aapl_data, "MSFT": msft_data}
spots = {"USD": 1, "AAPL": 227.75, "MSFT": 426.38}
weights = {"USD": 0.4, "AAPL": 0.3, "MSFT": 0.3}
initial_pool = 250000
balances = {asset: (initial_pool * weights[asset]) / spots[asset] for asset in assets}

#last_close_prices["AAPL"] = aapl_data['Open'].iloc[0]  # Initialize with the first available close
#last_close_msft = msft_data['Open'].iloc[0]  # Initialize with the first available close


# Fee values for different scenarios
#fee_values = [0.1, 0.25, 0.3, 0.4, 0.5, 0.75, 0.9, 1, 1.25, 1.5, 2, 2.5]
fee_values = [2]
results = []
trades = 0
direction = {}

def calculate_invariant(balances, weights):
    """Calculate invariant based on balances and weights."""
    inv = 1
    for asset in assets:
        inv *= balances[asset] ** weights[asset]
    return inv

def print_pool_standing(balances, inv, opens):
    print(f"Assets: {assets}")
    #print(f"Weights: {weights}")
    print(f"Balances: {balances}")
    print(f"Inv: {inv}")
    #print("Values: ")
    total_pool_value = 0
    for asset in assets:
        total_pool_value += balances[asset] * opens[asset]
        print("Asset ", asset, " value: ", balances[asset] * opens[asset])
        #inv *= balances[asset] ** weights[asset])
    print(f"Total pool value: {total_pool_value}")


# Loop through each fee variation
for fee_percentage in fee_values:
    fee = fee_percentage / 100
    # Initialize balances and invariant
    balances = {asset: (initial_pool * weights[asset]) / spots[asset] for asset in assets}


    trades_log = []
    end_of_period_values = []

    # Loop through each unique time period
    # Fetch data for each asset at the current time and update last close prices if needed
    open_prices = {}
    last_close_prices = {}
    for time in unique_times:
         #if trades > 10:
             #rint("breaking")
             #break

        print(time)
        #
        for asset in assets:
            if asset == "USD":
                open_prices[asset] = spots["USD"]
                last_close_prices[asset] = spots["USD"]
            else:
                direction[asset] = None
                asset_data = data[asset]
                row = asset_data[asset_data['Time'] == time]
                if not row.empty:
                    open_prices[asset] = row['Open'].values[0]
                    last_close_prices[asset] = row['Close'].values[0]
                else:
                    open_prices[asset] = last_close_prices[asset]

        # Trading loop for each asset
        continue_trading = True
        while continue_trading:
            continue_trading = False

            for asset in assets:
                if asset == "USD":
                    continue

                print(asset)

                # Fetch high and low prices for the asset
                row = data[asset][data[asset]['Time'] == time]
                if not row.empty:
                    high_price = row['High'].values[0]
                    low_price = row['Low'].values[0]

                    # Calculate bid and ask prices for the current asset
                    other_balances_product = 1
                    for other_asset in assets:
                        if other_asset != asset and other_asset != "USD":
                            #print("other asset: ", other_asset, " balance: ", balances[other_asset], " weight: ", weights[other_asset])
                            other_balances_product *= balances[other_asset] ** weights[other_asset]

                    inv = calculate_invariant(balances, weights)
                    #print("other asset balances produt: ", other_balances_product)
                    #print("balance of the asset: ", balances[asset])
                    #print("invariant: ", balances[asset]**weights[asset] * other_balances_product)
                    print(f"Balance: {balances[asset]}, weight: {weights[asset]}")
                    print(f"Inv: {inv}, Other bal product: {other_balances_product}")

                    bid_price = abs(((inv / ((balances[asset] + 1) ** weights[asset] * other_balances_product)) ** (1 / weights["USD"]) - balances["USD"]) * (1 - fee))
                    ask_price = abs(((inv / ((balances[asset] - 1) ** weights[asset] * other_balances_product)) ** (1 / weights["USD"]) - balances["USD"]) * (1 + fee))

                    print(asset, " bid: ", bid_price)
                    print(asset, " ask: ", ask_price)

                    # Execute trades based on bid/ask and market high/low prices
                    if high_price >= ask_price and direction[asset] != "buy":
                        # Sell asset
                        direction[asset] = "sell"
                        trades += 1
                        if True:
                            print("Trade: ", trades)
                            print_pool_standing(balances, inv, open_prices)
                            trades_log.append({'Time': time, 'Asset': asset, 'Action': 'Sell', 'Shares': 1, 'Price': ask_price})
                            print({'Time': time, 'Asset': asset, 'Action': 'Sell', 'Shares': 1, 'Price': ask_price})
                        balances["USD"] += ask_price
                        balances[asset] -= 1

                        inv = calculate_invariant(balances, weights)
                        if True:
                            print_pool_standing(balances, inv, open_prices)
                        continue_trading = True  # Check for more trades within the period

                    elif low_price <= bid_price and direction[asset] != "sell":
                        # Buy asset
                        direction[asset] = "buy"

                        if True:
                            trades += 1
                            print("Trade: ", trades)
                            print_pool_standing(balances, inv, open_prices)
                            trades_log.append({'Time': time, 'Asset': asset, 'Action': 'Buy', 'Shares': 1, 'Price': bid_price})
                            print({'Time': time, 'Asset': asset, 'Action': 'Buy', 'Shares': 1, 'Price': bid_price})
                        balances["USD"] -= bid_price
                        balances[asset] += 1

                        inv = calculate_invariant(balances, weights)
                        if True:
                            print_pool_standing(balances, inv, open_prices)
                        continue_trading = True  # Check for more trades within the period

        # Calculate end-of-period pool value
        pool_value = balances["USD"]
        for asset in assets:
            if asset != "USD":
                pool_value += balances[asset] * last_close_prices[asset]
        end_of_period_values.append(pool_value)

    # Record the final pool value for the current fee
    final_pool_value = end_of_period_values[-1]
    results.append({'Fee %': fee_percentage, 'Final_Pool_Value': final_pool_value})

# Convert results to DataFrame for comparison
results_df = pd.DataFrame(results)
print(results_df)
