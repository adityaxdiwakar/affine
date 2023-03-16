import pulp
import sys

done = False
print("reading from stdin...")

tickers = []
allocations = []
prices = []
for line in sys.stdin:
    if "exit" in line:
        print("exiting...")
        sys.exit(1)

    if (line.count(",") == 0):
        c = float(line)
        break
    [ticker, allocation, price] = line.split(",")
    tickers.append(ticker)
    allocations.append(float(allocation))
    prices.append(float(price))

print()
if sum(allocations) != 1:
    print("error: allocations do not sum to 1, exiting...")
    sys.exit(1)

N = len(tickers)

prob = pulp.LpProblem("stock_allocation", pulp.LpMinimize)
loss = pulp.LpVariable("loss")

allocs = pulp.LpVariable.dicts("x",range(N))
loss_idv = pulp.LpVariable.dicts("x_loss", range(N))
abs_idv = pulp.LpVariable.dicts("x_loss_abs", range(N))
reprs = pulp.LpVariable.dicts("x_qty", range(N), cat=pulp.LpInteger)
qty = pulp.LpVariable.dicts("x_qty_fin", range(N))

# net objective function (additionally constrained below)
prob += loss

# definition of loss
prob += loss == pulp.lpSum(abs_idv)

# subject to minimizing absolute distance from allocation target
for i in range(N):
    prob += loss_idv[i] == allocs[i] - allocations[i]
    prob += abs_idv[i] >= loss_idv[i]
    prob += abs_idv[i] >= -loss_idv[i]

# ensuring integer allocations
for i in range(N):
    multiplier = 1
    prob += reprs[i] == multiplier * (allocs[i] * c) / prices[i]
    prob += qty[i] == (1 / multiplier) * reprs[i]

# Solve the problem
prob.solve()

total_price = 0
total_allocd = 0
print("==========================")
print("here are your allocations:")
for i in range(N):
    lot_qty = qty[i].value()
    lot_price = round(prices[i] * lot_qty, 2)
    lot_alloc = round(100 * allocs[i].value(), 2)
    lot_error = round(lot_alloc - 100 * allocations[i], 2)
    total_price += lot_price
    total_allocd += lot_alloc
    print(f"\t{tickers[i].lower()}: {lot_qty} shares for ${lot_price:.2f} making up {lot_alloc}% [{lot_error}%]")
print(f"totalling ${total_price:.2f} for {total_allocd}% of portfolio")
