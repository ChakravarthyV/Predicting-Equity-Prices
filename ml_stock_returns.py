import requests
import json
import pandas as pd

#Enter a company's ticker, e.g.: IBM
ticker = input('TICKER: ')

#Retrieve balance sheet, income and cash flow statements using alphavantage's API, and convert them into json files
balance_sheet = (requests.get('https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=' + ticker + '&apikey=MLV8L40Q78HEXR2P')).json()
income_statement = (requests.get('https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=' + ticker + '&apikey=MLV8L40Q78HEXR2P')).json()
cash_flow = (requests.get('https://www.alphavantage.co/query?function=CASH_FLOW&symbol=' + ticker + '&apikey=MLV8L40Q78HEXR2P')).json()

"""
Each .json file above is made up of two dictionaries with keys 'symbol' and 'annualReports'. The latter's associated value 
is a list of more dictionaries -- with each dictionary made up of several key-value items for that respective fiscal year.
"""

def bs_parser():
    """
    For now, the bs_parser function returns a pandas dataframe with columns as fiscal year and corresponding b/s items.
    """
    bs_df = pd.DataFrame(balance_sheet['annualReports']) #why should i pass a list?
    
    return bs_df
    
def is_parser():
    """
    For now, the is_parser function returns a pandas dataframe with columns as fiscal year and corresponding i/s items.
    """
    is_df = pd.DataFrame(income_statement['annualReports'])
    
    return is_df

def cf_parser():
    """
    For now, the cf_parser function returns a pandas dataframe with columns as fiscal year and corresponding c/f items.
    """
    cf_df = pd.DataFrame(cash_flow['annualReports'])
    
    return cf_df

print(bs_parser()) #dimensions: 5x38
print(is_parser()) #5x26
print(cf_parser()) #5x28

