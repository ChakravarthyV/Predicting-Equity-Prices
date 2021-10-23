import requests
import json
import pandas as pd
import numpy as np

"""
Given the API's daily limit to the number of calls allowed, the purpose of this file is to 
test and train our model offline. It is assumed that you have the company's json-formatted balance sheet, 
income statement, and cash flow statement downloaded locally.
"""

#Locate offline accounting statements, assumes for now that the company is IBM
b_s = json.load(open('balance_sheet.json',))
i_s = json.load(open('income_statement.json',))
c_f = json.load(open('income_statement.json',))

#Convert json files into dataframes -- break them up into quarterly reports
bs_df = pd.DataFrame(b_s['quarterlyReports'])
is_df =  pd.DataFrame(i_s['quarterlyReports'])
cf_df = pd.DataFrame(c_f['quarterlyReports'])


df1 = pd.merge(is_df, cf_df, left_index=True, right_index=True, how='outer', suffixes=('', '_y')) #due to repeated columns in CF and IS, keep 2nd copies of repeating columns and non-repeating columns only
df1.drop(df1.filter(regex='_y$').columns.tolist(),axis=1, inplace=True) #now, remove portion of column names that show that it's a 2nd copy

#Company's quarterly reports collected and cleaned from all three accounting statements.
ibm_df = pd.merge(bs_df, df1, on=['fiscalDateEnding','reportedCurrency']) #merge BS with the cleaned up combination of CF and IS on the only two shared columns they have

#Loop through each column and replace any 'None' strings with the value NaN
for col in ibm_df.columns:
    ibm_df[col].replace('None', np.nan, inplace=True)

ibm_df = ibm_df.fillna(0) #fill up all NaN values with the integer 0

#Lo and behold, a company's quarterly filings merged across all three accounting statements, represented as a clean dataframe
print(ibm_df)

#Export dataframe into a csv (check it out yourself)
ibm_df.to_csv('sample.csv', encoding='utf-8', index=False)
