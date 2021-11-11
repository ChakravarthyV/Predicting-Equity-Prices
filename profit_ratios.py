import pandas as pd
#profitability ratios

#importing the csv file 
df = pd.read_csv (r'sample.csv')

#gross margin 
df1 = (df['grossProfit'] / df['totalRevenue']).to_frame('grossMargin')

print (df1)
