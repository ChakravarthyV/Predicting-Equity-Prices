import pandas as pd
import numpy as np
#Debt and Interest ratios

#Importing the csv file
df = pd.read_csv (r'sample.csv')
#create new dataframe with columns for each ratio
df2 = pd.DataFrame(columns=['interestCoverage', 'debtToCap', 'totalDebt'])

#Calculate each ratio and append to the respective column in the dataframe
df2['interestCoverage'] = df['ebit'] / df['interestExpense']
df2['debtToCap'] = df['longTermDebt'] / df['totalShareholderEquity']
df2['totalDebt'] = (df['shortTermDebt'] + df['longTermDebt']) / df['totalAssets']

#Start index from 1
df2.index = np.arange(1, len(df2)+1)
#Export dataframe into a csv 
df2.to_csv('debt_interest.csv', encoding='utf-8', index=False)
print (df2)