import pandas as pd

# Load AAPL and MSFT data
aapl_data = pd.read_excel("aapl_10-25-2024_1_min.xlsx")
msft_data = pd.read_excel("msft_25-10-2024_1_min.xlsx")
#print(aapl_data)
#print(msft_data)

# Convert 'Time' columns to datetime format
#aapl_data['Time'] = pd.to_datetime(aapl_data['Time'])
#msft_data['Time'] = pd.to_datetime(msft_data['Time'])
aapl_data['Time'] = pd.to_datetime(aapl_data['Time'], format="%m/%d/%Y %I:%M:%S %p")
msft_data['Time'] = pd.to_datetime(msft_data['Time'], format="%m/%d/%Y %I:%M:%S %p")


# Merge unique timestamps from both datasets and sort them
unique_times = pd.concat([aapl_data['Time'], msft_data['Time']]).drop_duplicates().sort_values()

# Initialize last known close prices for fallback
last_close_aapl = aapl_data['Open'].iloc[0]  # Initialize with the first available close
last_close_msft = msft_data['Open'].iloc[0]  # Initialize with the first available close


#print(unique_times)

# Initialize pool and other constants
assets = ["USD", "AAPL", "MSFT"]
pool = 250000
spots = [1, 227.75, 426.38]
weights = [0.4, 0.3, 0.3]
values = [pool * weights[0], pool * weights[1], pool * weights[2]]
#print(values)
fee_values = [2]  # Fees in percentage points

results = []
trade = 0

def print_pool_standing(balances, inv, opens):
    print(f"Assets: {assets}")
    #print(f"Weights: {weights}")
    print(f"Balances: {balances}")

    print(f"Inv: {inv}")
    print(f"Values: {balances[0]}, {balances[1] * opens[1]}, {balances[2] * opens[2]}")
    total_pool_value = balances[0] + balances[1] * opens[1] + balances[2] * opens[2]
    print(f"Total pool value: {total_pool_value}")

# Loop through each fee variation
for fee_percentage in fee_values:
    fee = fee_percentage / 100  # Convert to decimal form
    balances = [values[0], values[1] / spots[1], values[2] / spots[2]]
    #print(balances)
    inv = (balances[0] ** weights[0] * balances[1] ** weights[1] * balances[2] ** weights[2])
    #print(inv)

    trades_log = []
    end_of_period_values = []

    # Loop through each unique time period
    for time in unique_times:
        # Fetch data for the current time from both datasets
        aapl_row = aapl_data[aapl_data['Time'] == time]
        msft_row = msft_data[msft_data['Time'] == time]

        # Determine the open price for AAPL
        if not aapl_row.empty:
            open_price_aapl = aapl_row['Open'].values[0]
            last_close_aapl = aapl_row['Close'].values[0]  # Update last close for future periods
        else:
            open_price_aapl = last_close_aapl  # Use last known close price

        # Determine the open price for MSFT
        if not msft_row.empty:
            open_price_msft = msft_row['Open'].values[0]
            last_close_msft = msft_row['Close'].values[0]  # Update last close for future periods
        else:
            open_price_msft = last_close_msft  # Use last known close price

        # Initialize trade types for each asset
        trade_type_aapl = None  # Trade type for AAPL: None, 'buy', or 'sell'
        trade_type_msft = None  # Trade type for MSFT: None, 'buy', or 'sell'
        continue_trading = True  # To control the re-evaluation loop

        while continue_trading:
            continue_trading = False  # Assume no trades initially for this loop

            # Process AAPL if data is available
            if not aapl_row.empty:
                high_price_aapl = aapl_row['High'].values[0]
                low_price_aapl = aapl_row['Low'].values[0]
                close_price_aapl = aapl_row['Close'].values[0]
                #open_price_aapl = aapl_row['Open'].values[0]

                # Calculate bid and ask for AAPL
                bid_aapl = abs(((inv / ((balances[1] + 1) ** weights[1] * balances[2] ** weights[2])) ** (1 / weights[0]) - balances[0]) * (1 - fee))
                ask_aapl = abs(((inv / ((balances[1] - 1) ** weights[1] * balances[2] ** weights[2])) ** (1 / weights[0]) - balances[0]) * (1 + fee))
                #print(f"AAPL bid: {bid_aapl}")
                #print(f"AAPL ask: {ask_aapl}")

                # Attempt trades on AAPL
                if high_price_aapl >= ask_aapl and trade_type_aapl in [None, 'sell']:
                    trade += 1
                    print(f"Trade: {trade}")
                    trade_type_aapl = 'sell'
                    print_pool_standing(balances, inv, [1, open_price_aapl, open_price_msft])
                    balances[0] += ask_aapl
                    balances[1] -= 1

                    trades_log.append({'Time': time, 'Asset': 'AAPL', 'Action': 'Sell', 'Shares': 1, 'Price': ask_aapl})
                    print({'Time': time, 'Asset': 'AAPL', 'Action': 'Sell', 'Shares': 1, 'Price': ask_aapl})
                    inv = (balances[0] ** weights[0] * balances[1] ** weights[1] * balances[2] ** weights[2])
                    print_pool_standing(balances, inv, [1, open_price_aapl, open_price_msft])
                    ask_aapl = abs(((inv / ((balances[1] - 1) ** weights[1] * balances[2] ** weights[2])) ** (1 / weights[0]) - balances[0]) * (1 + fee))

                    continue_trading = True  # Re-evaluate trades for other assets

                elif low_price_aapl <= bid_aapl and trade_type_aapl in [None, 'buy']:
                    trade += 1
                    print(f"Trade: {trade}")
                    trade_type_aapl = 'buy'
                    print_pool_standing(balances, inv, [1, open_price_aapl, open_price_msft])
                    balances[0] -= bid_aapl
                    balances[1] += 1
                    trades_log.append({'Time': time, 'Asset': 'AAPL', 'Action': 'Buy', 'Shares': 1, 'Price': bid_aapl})
                    print({'Time': time, 'Asset': 'AAPL', 'Action': 'Buy', 'Shares': 1, 'Price': bid_aapl})
                    inv = (balances[0] ** weights[0] * balances[1] ** weights[1] * balances[2] ** weights[2])
                    print_pool_standing(balances, inv, [1, open_price_aapl, open_price_msft])
                    bid_aapl = abs(((inv / ((balances[1] + 1) ** weights[1] * balances[2] ** weights[2])) ** (1 / weights[0]) - balances[0]) * (1 - fee))
                    continue_trading = True

            # Process MSFT if data is available
            if not msft_row.empty:
                high_price_msft = msft_row['High'].values[0]
                low_price_msft = msft_row['Low'].values[0]
                close_price_msft = msft_row['Close'].values[0]
                #open_price_msft = msft_row['Open'].values[0]

                # Calculate bid and ask for MSFT
                bid_msft = abs(((inv / ((balances[2] + 1) ** weights[2] * balances[1] ** weights[1])) ** (1 / weights[0]) - balances[0]) * (1 - fee))
                ask_msft = abs(((inv / ((balances[2] - 1) ** weights[2] * balances[1] ** weights[1])) ** (1 / weights[0]) - balances[0]) * (1 + fee))

                # Attempt trades on MSFT
                if high_price_msft >= ask_msft and trade_type_msft in [None, 'sell']:
                    trade += 1
                    print(f"Trade: {trade}")
                    trade_type_msft = 'sell'
                    print_pool_standing(balances, inv, [1, open_price_aapl, open_price_msft])
                    balances[0] += ask_msft
                    balances[2] -= 1
                    trades_log.append({'Time': time, 'Asset': 'MSFT', 'Action': 'Sell', 'Shares': 1, 'Price': ask_msft})
                    print({'Time': time, 'Asset': 'MSFT', 'Action': 'Sell', 'Shares': 1, 'Price': ask_msft})

                    inv = (balances[0] ** weights[0] * balances[1] ** weights[1] * balances[2] ** weights[2])
                    print_pool_standing(balances, inv, [1, open_price_aapl, open_price_msft])
                    ask_msft = abs(((inv / ((balances[2] - 1) ** weights[2] * balances[1] ** weights[1])) ** (1 / weights[0]) - balances[0]) * (1 + fee))
                    continue_trading = True

                elif low_price_msft <= bid_msft and trade_type_msft in [None, 'buy']:
                    trade += 1
                    print(f"Trade: {trade}")
                    trade_type_msft = 'buy'
                    print_pool_standing(balances, inv, [1, open_price_aapl, open_price_msft])
                    balances[0] -= bid_msft
                    balances[2] += 1
                    #print(f"inv1: {balances[0] ** weights[0]}")
                    #print(f"inv2: {balances[1] ** weights[1]}")
                    #print(f"inv3: {balances[2] ** weights[2]}")

                    trades_log.append({'Time': time, 'Asset': 'MSFT', 'Action': 'Buy', 'Shares': 1, 'Price': bid_msft})
                    print({'Time': time, 'Asset': 'MSFT', 'Action': 'Buy', 'Shares': 1, 'Price': bid_msft})
                    inv = (balances[0] ** weights[0] * balances[1] ** weights[1] * balances[2] ** weights[2])
                    #print(f"inv: {inv}")
                    #print(f"new bal: {(balances[2] + 1)}")
                    #print(f"weight: {weights[2]}")
                    #print(f"other asset: {balances[1] ** weights[1]}")
                    #rint(f"Number: {(inv / (balances[2] + 1) ** weights[2] * balances[1] ** weights[1])}")

                    bid_msft = abs(((inv / ((balances[2] + 1) ** weights[2] * balances[1] ** weights[1])) ** (1 / weights[0]) - balances[0]) * (1 - fee))

                    print_pool_standing(balances, inv, [1, open_price_aapl, open_price_msft])
                    continue_trading = True

        # End-of-period pool value for each time period
        pool_value = balances[0] + (balances[1] * last_close_aapl if not aapl_row.empty else 0) + (balances[2] * last_close_msft if not msft_row.empty else 0)
        end_of_period_values.append(pool_value)

    # Record final pool value after all periods
    final_pool_value = end_of_period_values[-1]
    results.append({'Fee %': fee_percentage, 'Final_Pool_Value': final_pool_value})

# Convert results to DataFrame for comparison
results_df = pd.DataFrame(results)
print(results_df)
