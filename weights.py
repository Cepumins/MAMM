def calculate_ask_bid_prices(y, w_y, x, w_x):
    # Calculate the constant k
    inv = (y ** w_y) * (x ** w_x)
    print(f"Invariant: {inv}")

    # Calculate ask price
    #y_new_ask = k / (x - 1)
    #ask = y_new_ask - y

    # Calculate bid price
    #y_new_bid = k / (x + 1)
    #bid = y - y_new_bid
    ask = (inv / (x - 1) ** w_x) ** (1 / w_y) - y
    bid = y - (inv / (x + 1) ** w_x) ** (1 / w_y)

    print(f"Ask Price: {ask}")
    print(f"Bid Price: {bid}")

y = 50
w_y = 0.5

x = 100
w_x = 0.5


calculate_ask_bid_prices(y, w_y, x, w_x)

calculate_ask_bid_prices(240, 0.5, 5, 0.5)
