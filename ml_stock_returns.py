import requests
import json

#Enter a company's ticker, e.g.: IBM
ticker = input('TICKER: ')

#Retrieve balance sheet, income and cash flow statements using alphavantage's API, and convert them into json-formatted files
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