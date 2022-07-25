import numpy as np
import pandas as pd
import math
import requests
import xlsxwriter
from scipy import stats
from IEX import IEX_CLOUD_API_TOKEN
from statistics import mean

stocks = pd.read_csv("./sp_500_stocks.csv")
stocks = stocks[~stocks['Ticker'].isin(['DISCA','HFC','VIAC','WLTW'])]

def make_sublist(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]   

symbol_groups = list(make_sublist(stocks["Ticker"], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

def portfolio_input():
    global portfolio_size
    portfolio_size = input("Enter the size of your portfolio")
    try:
        float(portfolio_size)
    except ValueError:
        print("That is not a number \nPlease try again:")
        portfolio_size = input("Enter the size of your portfolio")
portfolio_input()

hqm_columns= ["Ticker", 
                "Price", 
                "Number of shares to Buy", 
                "One-Year Price Return", 
                "One-Year Return Percentile", 
                'Six-Month Price Return',
                'Six-Month Return Percentile',
                'Three-Month Price Return',
                'Three-Month Return Percentile',
                'One-Month Price Return',
                'One-Month Return Percentile',
                'HQM Score' ]
hqm_dataframe = pd.DataFrame(columns = hqm_columns)

for symbol_string in symbol_strings:
    data = requests.get(f"https://sandbox.iexapis.com/stable/stock/market/batch?types=stats,quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}").json()
    for symbol in symbol_string.split(','):
        hqm_dataframe = hqm_dataframe.append(
            pd.Series(
                [
                symbol, 
                data[symbol]['quote']['latestPrice'],
                'N/A',
                data[symbol]['stats']['year1ChangePercent'],
                'N/A',
                data[symbol]['stats']['month6ChangePercent'],
                'N/A',
                data[symbol]['stats']['month3ChangePercent'],
                'N/A',
                data[symbol]['stats']['month1ChangePercent'],
                'N/A',
                'N/A' 
                ], index = hqm_columns
            ), ignore_index=True 
        )

time_periods = [
    "One-Year",
    "Six-Month",
    "Three-Month",
    "One-Month"
]

for row in hqm_dataframe.index:
    for time_period in time_periods:
    
        change_col = f'{time_period} Price Return'
        percentile_col = f'{time_period} Return Percentile'
        if hqm_dataframe.loc[row, change_col] == None:
            hqm_dataframe.loc[row, change_col] = 0.0
            
for row in hqm_dataframe.index:
    for time_period in time_periods:
        change_col = f'{time_period} Price Return'
        percentile_col = f'{time_period} Return Percentile'
        hqm_dataframe.loc[row, percentile_col] = stats.percentileofscore(hqm_dataframe[change_col], hqm_dataframe.loc[row, change_col])

for row in hqm_dataframe.index:
    momentum_percentiles =[]
    for time_period in time_periods:
        momentum_percentiles.append(hqm_dataframe.loc[row, f"{time_period} Return Percentile"])
    hqm_dataframe.loc[row, 'HQM Score'] = mean(momentum_percentiles)

hqm_dataframe.sort_values("HQM Score", ascending=False, inplace=True)
hqm_dataframe = hqm_dataframe[:50]
hqm_dataframe.reset_index(drop=True, inplace=True,)

writer = pd.ExcelWriter("momentum strategy.xlsx", engine = "xlsxwriter")
hqm_dataframe.to_excel(writer, sheet_name= "Momentum Strategy", index = False)
background_color = '#0a0a23'
font_color = '#ffffff'

string_template = writer.book.add_format(
        {
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

dollar_template = writer.book.add_format(
        {
            'num_format':'$0.00',
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

integer_template = writer.book.add_format(
        {
            'num_format':'0',
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

percent_template = writer.book.add_format(
        {
            'num_format':'0.0%',
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

column_formats = { 
                    'A': ['Ticker', string_template],
                    'B': ['Price', dollar_template],
                    'C': ['Number of Shares to Buy', integer_template],
                    'D': ['One-Year Price Return', percent_template],
                    'E': ['One-Year Return Percentile', percent_template],
                    'F': ['Six-Month Price Return', percent_template],
                    'G': ['Six-Month Return Percentile', percent_template],
                    'H': ['Three-Month Price Return', percent_template],
                    'I': ['Three-Month Return Percentile', percent_template],
                    'J': ['One-Month Price Return', percent_template],
                    'K': ['One-Month Return Percentile', percent_template],
                    'L': ['HQM Score', integer_template]
                    }

for column in column_formats.keys():
    writer.sheets['Momentum Strategy'].set_column(f'{column}:{column}', 20, column_formats[column][1])
    writer.sheets['Momentum Strategy'].write(f'{column}1', column_formats[column][0], string_template)

writer.save()