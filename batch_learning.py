import json
import pandas as pd
import numpy as np
import yfinance as yf
import datetime

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics


"""
Acquire financial datasets.
"""
#IBM's price history
price_df = yf.download("IBM", start="2014-01-01", end="2021-11-1") #YYYY-MM-DD
price_df = price_df.reset_index() #set 'Date' as column

#convert json to pd
bs_json = json.load(open('balance_sheet.json',))
is_json = json.load(open('income_statement.json',))
cf_json = json.load(open('cash_flow.json',))
bs_df = pd.DataFrame(bs_json['quarterlyReports'])
is_df =  pd.DataFrame(is_json['quarterlyReports'])
cf_df = pd.DataFrame(cf_json['quarterlyReports'])


"""
Clean and merge into one workable dataset.
"""
#merge balance sheet, income statement, and cash flow statement into one sizeable df
df1 = pd.merge(is_df, cf_df, left_index=True, right_index=True, how='outer', suffixes=('', '_y')) #keep 2nd copies of repeating columns only
df1.drop(df1.filter(regex='_y$').columns.tolist(),axis=1, inplace=True) #remove portion of column names that show that it's a 2nd copy
refined_df = pd.merge(bs_df, df1, on=['fiscalDateEnding','reportedCurrency']) 

for col in refined_df.columns: #loop through each column and replace any 'None' strings with the value NaN
    refined_df[col].replace('None', np.nan, inplace=True)
refined_df = refined_df.fillna(0) #fill up all NaN values with the integer 0
refined_df['fiscalDateEnding'] =  pd.to_datetime(refined_df['fiscalDateEnding']) #convert date column to datetime

#function to find nearest date
def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))
dates_list = []
for quarter_date in refined_df['fiscalDateEnding']:
    dates_list.append(nearest(price_df['Date'].to_list(), quarter_date)) #find dates in yfinance data closest matching those of quarterly filings
prices_list = []
for date in dates_list:
    prices_list.append(price_df.loc[price_df['Date'] == date, 'Close'].item()) #for those dates, get closing day stock prices
refined_df['stockPrice'] = prices_list #set stock prices as new df

cols = refined_df.columns
refined_df[cols[2:]] = refined_df[cols[2:]].apply(pd.to_numeric, errors='coerce') #convert all columns except first two to type int


"""
Use workable dataset to create features + target variables dataset.
"""
dataset_df = pd.DataFrame()
def ratio_calculator(df):
    """
    Takes in refined_df and returns operable_df.
    """
    #Price
    dataset_df['stockPrice'] = df['stockPrice']
    
    #Stock Evaluation
    market_cap = df['stockPrice']*df['commonStockSharesOutstanding']
    enterprise_value = market_cap + (df['shortTermDebt'] + df['longTermDebt']) - df['cashAndShortTermInvestments']
    dataset_df['ebitToEV'] = df['ebit']/enterprise_value
    dataset_df['earningsToPrice'] = df['netIncome']/market_cap #P/E inverse
    dataset_df['dividendYield'] = df['dividendPayoutCommonStock']/market_cap

    #Profitability
    dataset_df['grossMargin'] = df['grossProfit']/df['totalRevenue']
    dataset_df['operProfitMargin'] = df['ebitda']/df['totalRevenue']
    dataset_df['pretaxProfitMargin'] = df['incomeBeforeTax']/df['totalRevenue']
    dataset_df['netProfitMargin'] = df['netIncome']/df['totalRevenue']
    dataset_df['returnInvestedCapital'] = df['netIncome']/(df['shortTermDebt']+df['longTermDebt']+df['totalShareholderEquity'])
    dataset_df['returnOnEquity'] = df['netIncome']/df['totalShareholderEquity']
    dataset_df['returnOnAssets'] = df['netIncome']/df['totalAssets']

    #Financial Condition
    dataset_df['currentRatio'] = df['totalCurrentAssets']/df['totalCurrentLiabilities']
    dataset_df['quickRatio'] = (df['totalCurrentAssets'] - df['inventory'])/df['totalCurrentLiabilities']
    dataset_df['cashRatio'] = df['cashAndShortTermInvestments']/df['totalCurrentLiabilities']

    #Efficiency
    dataset_df['assetTurnover'] = df['totalRevenue']/df['totalAssets']
    dataset_df['inventoryTurnover'] = df['totalRevenue']/df['inventory']
    dataset_df['receivablesTurnover'] = df['totalRevenue']/df['currentNetReceivables']

    #Debt and Interest
    dataset_df['interestCoverage'] = df['interestExpense']/df['ebit']
    dataset_df['debtToCap'] = df['longTermDebt']/(df['totalShareholderEquity'] + df['longTermDebt'])
    dataset_df['debtToAssets'] = (df['shortTermDebt'] + df['longTermDebt']) / df['totalAssets']
    
    return dataset_df

ratio_calculator(refined_df)


"""
Decision Tree.
"""
X = dataset_df.iloc[:, 1:].values
y = dataset_df.iloc[:, 0].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=0)
regressor = RandomForestRegressor(n_estimators=15, random_state=0) #total number of decision trees: 15
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))