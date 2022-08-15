# Financial-Algorithms

This repository contains three trading algorithms
All of these projects are made using Python, a couple of its libraries: Numpy, Pandas, xlsxwriter, and requests, and the IEX cloud API  

# 1. Equal weight index fund (sp_500)

This project contains the algorithm to invest in an equal weight index fund consisting of all the stocks included in the S&P500. Based off the portfolio amount entered by the user the script returns an excel file listing the amount of money that should be invested by the user to have the exact amount of weightage for each stock in the index fund.

# 2. Quantitative momentum investing strategy (quant_moment)

This project is based off momentum investing i.e. the strategy to invest in stocks that have increased in price the most. To identify high quality momentum stocks the stocks are selected from the highest percentiles of four factors: 
* 1-month price returns
* 3-month price returns
* 6-month price returns
* 1-year price returns
