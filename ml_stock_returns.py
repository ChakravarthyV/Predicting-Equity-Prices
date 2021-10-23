import requests
import json
import pandas as pd

#Enter a company's ticker, e.g.: IBM
ticker = input('TICKER: ')

"""
This is the main document. Can be used to call and download json-formatted accounting statements
using alphadvantage's API. Once stored offline, the batch_learning.py file is used to parse locally-kept
data files. 
"""
#Retrieve balance sheet, income and cash flow statements using alphadvantage's API, and convert them into json files
balance_sheet = (requests.get('https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=' + ticker + '&apikey=MLV8L40Q78HEXR2P'))
income_statement = (requests.get('https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=' + ticker + '&apikey=MLV8L40Q78HEXR2P'))
cash_flow = (requests.get('https://www.alphavantage.co/query?function=CASH_FLOW&symbol=' + ticker + '&apikey=MLV8L40Q78HEXR2P'))


with open('balance_sheet.json', 'wb') as outf:
    outf.write(balance_sheet.content)

with open('income_statement.json', 'wb') as outf:
    outf.write(income_statement.content)

with open('cash_flow.json', 'wb') as outf:
    outf.write(cash_flow.content)

print(balance_sheet, income_statement, cash_flow) 

"""
Each .json file above is made up of two dictionaries with keys 'symbol' and 'annualReports'. The latter's associated value 
is a list of more dictionaries -- with each dictionary made up of several key-value items for that respective fiscal year.
"""




