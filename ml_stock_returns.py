import requests

#Enter a company's ticker, e.g.: IBM
ticker = input('TICKER: ')

#Retrieve balance sheet, income and cash flow statements using alphavantage's API, and convert them into json-formatted files
balance_sheet = (requests.get('https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=' + ticker + '&apikey=MLV8L40Q78HEXR2P')).json()
income_statement = (requests.get('https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=' + ticker + '&apikey=MLV8L40Q78HEXR2P')).json()
cash_flow = (requests.get('https://www.alphavantage.co/query?function=CASH_FLOW&symbol=' + ticker + '&apikey=MLV8L40Q78HEXR2P')).json()

print(balance_sheet, income_statement, cash_flow)