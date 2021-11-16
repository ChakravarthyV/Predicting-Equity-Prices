import requests
import json
import pandas as pd
import numpy as np
import yfinance as yf
import datetime

#function to find nearest date
def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

#offline training
price_df = yf.download("IBM", start="2014-01-01", end="2021-11-1") #YYYY-MM-DD
price_df = price_df.reset_index() #set 'Date' as column
price_df.to_csv('uhhh.csv', encoding='utf-8', index=False)

#sample case: IBM
bs_json = json.load(open('balance_sheet.json',))
is_json = json.load(open('income_statement.json',))
cf_json = json.load(open('income_statement.json',))

#convert json files into dataframes -- break them up into quarterly reports
bs_df = pd.DataFrame(bs_json['quarterlyReports'])
is_df =  pd.DataFrame(is_json['quarterlyReports'])
cf_df = pd.DataFrame(cf_json['quarterlyReports'])
df1 = pd.merge(is_df, cf_df, left_index=True, right_index=True, how='outer', suffixes=('', '_y')) #keep 2nd copies of repeating columns only
df1.drop(df1.filter(regex='_y$').columns.tolist(),axis=1, inplace=True) #remove portion of column names that show that it's a 2nd copy

#Company's quarterly reports collected and cleaned from all three accounting statements.
refined_df = pd.merge(bs_df, df1, on=['fiscalDateEnding','reportedCurrency']) #merge BS with the cleaned up combination of CF and IS on the only two shared columns they have

#Loop through each column and replace any 'None' strings with the value NaN
for col in refined_df.columns:
    refined_df[col].replace('None', np.nan, inplace=True)
refined_df = refined_df.fillna(0) #fill up all NaN values with the integer 0
refined_df['fiscalDateEnding'] =  pd.to_datetime(refined_df['fiscalDateEnding']) #convert date column to datetime

dates_list = []
for quarter_date in refined_df['fiscalDateEnding']:
    dates_list.append(nearest(price_df['Date'].to_list(), quarter_date)) #find dates in yfinance data closest matching those of quarterly filings

prices_list = []
for date in dates_list:
    prices_list.append(price_df.loc[price_df['Date'] == date, 'Close'].item()) #for those dates, get closing day stock prices

refined_df['stockPrice'] = prices_list #set stock prices as new df

#Export dataframe into a csv (check it out yourself)
refined_df.to_csv('sample.csv', encoding='utf-8', index=False)
