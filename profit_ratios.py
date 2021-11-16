import pandas as pd
#Profitability ratios

#Importing the csv file 
df = pd.read_csv (r'sample.csv')
#create empty dataframe
df1 = pd.DataFrame()

#Calculate each ratio and append to the respective column in the dataframe
df1['grossMargin'] = df['grossProfit']/df['totalRevenue']
df1['operProfitMargin'] = df['ebitda']/df['totalRevenue']
df1['pretaxProfitMargin'] = df['incomeBeforeTax']/df['totalRevenue']
df1['netProfitMargin'] = df['netIncome']/df['totalRevenue']
df1['returnInvestedCapital'] = df['netIncome']/(df['shortTermDebt']+df['longTermDebt']+df['totalShareholderEquity'])
df1['returnOnEquity'] = df['netIncome']/df['totalShareholderEquity']
df1['returnOnAssets'] = df['netIncome']/df['totalAssets']

#Export dataframe into a csv 
df1.to_csv('profit_ratios.csv', encoding='utf-8', index=False)
print (df1)
