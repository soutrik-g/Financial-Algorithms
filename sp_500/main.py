import math
import numpy as np
import pandas as pd
import xlsxwriter
import requests
from IEX import IEX_CLOUD_API_TOKEN 

stocks = pd.read_csv('./sp_500_stocks.csv')
stocks = stocks[~stocks['Ticker'].isin(['DISCA','HFC','VIAC','WLTW'])]
my_columns = ['Tickets', 'Stock Price', 'Market Capitalization', 'Number of shares to Buy']
final_dataframe = pd.DataFrame([[0, 0, 0, 0]], columns=my_columns)

def make_sublist(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

symbol_groups = list(make_sublist(stocks['Ticker'], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))
final_dataframe = pd.DataFrame(columns=my_columns)

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        final_dataframe = final_dataframe.append(
        pd.Series(
            [
            symbol,
            data[symbol]['quote']['latestPrice'],
            data[symbol]['quote']['marketCap'],
            'N/A'
            ],
            index = my_columns
        ),
        ignore_index = True
    )

portfolio_size = input("Enter the size of your portfolio:")
try:
    val = float(portfolio_size)
    print(val)
except ValueError:
    print("Not a number! \nPlease try again:")
    portfolio_size = input("Enter the size of your portfolio:")

position_size = val/len(final_dataframe.index)
for i in range(0,len(final_dataframe.index)):
    final_dataframe.loc[i, "Number of shares to Buy"] = math.floor(position_size/final_dataframe.loc[i,"Stock Price"])

writer = pd.ExcelWriter("trades.xlsx", engine = "xlsxwriter")
final_dataframe.to_excel(writer, "Trades", index = False)

background_color = "#0a0a23"
font_color = "#ffffff"
string_format = writer.book.add_format(
    {
        "font_color": font_color,
        "background_color": background_color,
        "border": 1

    }
)
dollar_format = writer.book.add_format(
    {
        "num_format": "$0.00",
        "font_color": font_color,
        "background_color": background_color,
        "border": 1

    }
)
integer_format = writer.book.add_format(
    {
        "num-format": "0",
        "font_color": font_color,
        "background_color": background_color,
        "border": 1

    }
)


column_formats = {
    'A': ["Ticker", string_format],
    'B': ["Stock Price", dollar_format],
    'C': ['Market Capitalizaion', dollar_format],
    'D': ["Number of shares to buy", integer_format]
}
for column in column_formats.keys():
    writer.sheets['Trades'].set_column(f'{column}:{column}', 20, column_formats[column][1])
    writer.sheets['Trades'].write(f'{column}1', column_formats[column][0], string_format)

writer.save()
