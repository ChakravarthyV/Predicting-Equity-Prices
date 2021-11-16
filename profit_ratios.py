import pandas as pd
import numpy as np
#Profitability ratios

#Importing the csv file 
df = pd.read_csv (r'sample.csv')
#create new dataframe with columns for each ratio
df1 = pd.DataFrame(columns=['grossMargin', 'operProfitMargin', 'pretaxProfitMargin', 'netProfitMargin', 'returnInvestedCapital', 'returnOnEquity', 'returnOnAssets'])

#Calculate each ratio and append to the respective column in the dataframe
df1['grossMargin'] = df['grossProfit'] / df['totalRevenue']
df1['operProfitMargin'] = df['ebitda'] / df['totalRevenue']
df1['pretaxProfitMargin'] = df['incomeBeforeTax']
df1['netProfitMargin'] = df['netIncome'] - df['incomeTaxExpense']
df1['returnInvestedCapital'] = (df['shortTermDebt'] + df['longTermDebt']) / df['totalShareholderEquity']
df1['returnOnEquity'] = df['netIncome'] / df['totalShareholderEquity']
df1['returnOnAssets'] = df['netIncome'] / df['totalAssets']

#Start index from 1
df1.index = np.arange(1, len(df1)+1)
#Export dataframe into a csv 
df1.to_csv('profit_ratios.csv', encoding='utf-8', index=False)
print (df1)
