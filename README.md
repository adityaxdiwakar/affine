# affine
Affine is a portfolio allocation utility that takes a list of stock allocations and market data and generates an optimal integer quantity of shares to purchase for each allocation. Affine uses linear programming and minimizes the allocation error that comes from using integer-only share allocations.

## Usage
You can run affine by doing
```sh
git clone git@github.com:adityaxdiwakar/affine.git
cd affine
python3 -m pip install pulp
python3 main.py
```

The execution reads `stdin` to get a comma separated triplets of stock tickers, allocation percentages, and stock prices. The last line (the only non-triplet) is the amount of money to be allocated. An example input is in `example_input.csv`. It is recommended to store inputs in a file, and use affine by piping the file into affine, like so:
```sh
python3 main.py < example_input.csv
```
This will yield some optimization outputs from `pulp` and end with
```
here are your allocations:
        aapl: 4.0 shares for $623.40 making up 4.88% [-0.12%]
        msft: 2.0 shares for $552.40 making up 4.32% [-0.68%]
        unh: 2.0 shares for $944.04 making up 7.39% [-0.61%]
        cost: 4.0 shares for $1949.04 making up 15.26% [0.26%]
        sbux: 13.0 shares for $1305.59 making up 10.22% [0.22%]
        googl: 9.0 shares for $902.88 making up 7.07% [0.07%]
        jpm: 10.0 shares for $1307.50 making up 10.23% [0.23%]
        voo: 14.0 shares for $5094.04 making up 39.88% [-0.12%]
totalling $12678.89 for 99.25% of portfolio
```

### Notes
affine is published as an integer allocator. If, instead, you are ok with half-share or tenth-share increements, then affine supports this as well. Simply change the `multiplier` in `main.py` from `1` using `multiplier = 1 / interval`. For example, if `interval = 0.5`, then `multiplier = 1 / 0.2 = 2`.

### Why?
If you use fractional shares, affine is not useful. When I managed smaller accounts, diversification of my accounts implied the usage of fractional shares. However, fractional shares sometimes come with a cost. When fractional shares are executed, brokerages execute whole-lot orders separately from fractional orders. For taxation purposes, this ends up as two distinct lots and also two completely different executions with different prices. The fill quality on fractional shares (empirically) is not great. Since I manage significantly larger accounts now, the utility of fractional shares is close to 0 as I can diversify without needing fractional quantities.

#### Why not floor single stock allocated quantities?
This works, but is a bit lossy as the amount of money "unallocated" from flooring the quantity cannot be reallocated elsewhere. From empiral testing, affine is able to allocate on average 99.25% of a $10,000 portfolio, while flooring yields 92.82% accuracy. More testing to come.
