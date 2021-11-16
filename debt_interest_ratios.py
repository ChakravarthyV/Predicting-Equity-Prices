import pandas as pd
#Debt and Interest ratios

#Importing the csv file
df = pd.read_csv (r'sample.csv')
#create empty dataframe
df2 = pd.DataFrame()

#Calculate each ratio and append to the respective column in the dataframe
df2['interestCoverage'] = df['interestExpense']/df['ebit']
df2['debtToCap'] = df['longTermDebt']/(df['totalShareholderEquity'] + df['longTermDebt'])
df2['debtToAssets'] = (df['shortTermDebt'] + df['longTermDebt']) / df['totalAssets']

#Export dataframe into a csv 
df2.to_csv('debt_interest.csv', encoding='utf-8', index=False)
print(df2)