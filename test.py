

other_balances_product = 471.6060105093215
weights = [0.3]
initial_pool = 250000
balances = [329.3084522502744]
print(balances)
usd_balance = initial_pool * 0.4
fee = 0.002
print(usd_balance)

print("other asset balances produt: ", other_balances_product)
inv = other_balances_product * (balances[0]**weights[0])
print("invariant: ", inv)

bid_price = abs((((inv / ((balances[0] + 1) ** weights[0] * other_balances_product)) ** (1 / 0.4)) - usd_balance) * (1 - fee))
ask_price = abs(((inv / ((balances[0] - 1) ** weights[0] * other_balances_product)) ** (1 / 0.4) - usd_balance) * (1 + fee))

print(bid_price)
print(ask_price)

print((inv / ((balances[0] + 1) ** weights[0] * other_balances_product)) ** (1 / 0.4))
