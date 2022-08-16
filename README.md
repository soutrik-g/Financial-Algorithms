# Financial-Algorithms

This repository contains three trading algorithms
All of these projects are made using Python, a couple of its libraries: Numpy, Pandas, xlsxwriter, and requests, and the IEX cloud API  

# 1. Equal weight index fund (sp_500)

This project contains the algorithm to invest in an equal weight index fund consisting of all the stocks included in the S&P500. Based off the portfolio amount entered by the user the script returns an excel file listing the amount of money that should be invested by the user to have the exact amount of weightage for each stock in the index fund.

# 2. Quantitative momentum investing strategy (quant_momentum)

This project is based off of momentum investing i.e. the strategy to invest in stocks that have increased in price the most. To identify high quality momentum stocks the stocks are selected from the highest percentiles of four factors: 
* 1-month price returns
* 3-month price returns
* 6-month price returns
* 1-year price returns
This data is then grabbed from the IEX API and then assigned momentum percentile scores, the arithmetic mean of the percentile scores is used to decide the 50 best such stocks to buy and then the portfolio size is used to build an equal weight portfolio of these stocks.

# 3. Quantitative value investing strategy (quant_value)

This project is based off of value investing i.e. the strategy to invest in stocks that have the lowest cost compared to business value measures. To identify the best value stocks the stocks are filtered from the lowest percentiles on these metrics : 
* Price-to-earnings ratio
* Price-to-book ratio
* Price-to-sales ratio
* Enterprise Value divided by Earnings Before Interest, Taxes, Depreciation, and Amortization (EV/EBITDA)
* Enterprise Value divided by Gross Profit (EV/GP)
Some of this data is not available through the API and so must be computed after the call, the arithmetic mean of the percentile scores is used to decide the 50 best stocks and then the portfolio size is used to build an equal weight portfolio of these stocks.
