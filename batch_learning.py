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

#sample case: IBM
bs_json = json.load(open('balance_sheet.json',))
is_json = json.load(open('income_statement.json',))
cf_json = json.load(open('cash_flow.json',))

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

cols = refined_df.columns
refined_df[cols[2:]] = refined_df[cols[2:]].apply(pd.to_numeric, errors='coerce') #convert all columns except first two to type int


##STOCK EVALUATION##
stock_eval_df = pd.DataFrame()
market_cap = refined_df['stockPrice']*refined_df['commonStockSharesOutstanding']
enterprise_value = market_cap + (refined_df['shortTermDebt'] + refined_df['longTermDebt']) - refined_df['cashAndShortTermInvestments']
stock_eval_df['ebitToEV'] = refined_df['ebit']/enterprise_value
stock_eval_df['earningsToPrice'] = refined_df['netIncome']/market_cap #P/E inverse
stock_eval_df['dividendYield'] = refined_df['dividendPayoutCommonStock']/market_cap

##PROFITABILITY##
profit_df = pd.DataFrame()
profit_df['grossMargin'] = refined_df['grossProfit']/refined_df['totalRevenue']
profit_df['operProfitMargin'] = refined_df['ebitda']/refined_df['totalRevenue']
profit_df['pretaxProfitMargin'] = refined_df['incomeBeforeTax']/refined_df['totalRevenue']
profit_df['netProfitMargin'] = refined_df['netIncome']/refined_df['totalRevenue']
profit_df['returnInvestedCapital'] = refined_df['netIncome']/(refined_df['shortTermDebt']+refined_df['longTermDebt']+refined_df['totalShareholderEquity'])
profit_df['returnOnEquity'] = refined_df['netIncome']/refined_df['totalShareholderEquity']
profit_df['returnOnAssets'] = refined_df['netIncome']/refined_df['totalAssets']

##FINANCIAL CONDITION##
fin_cond_df = pd.DataFrame()
fin_cond_df['currentRatio'] = refined_df['totalCurrentAssets']/refined_df['totalCurrentLiabilities']
fin_cond_df['quickRatio'] = (refined_df['totalCurrentAssets'] - refined_df['inventory'])/refined_df['totalCurrentLiabilities']
fin_cond_df['cashRatio'] = refined_df['cashAndShortTermInvestments']/refined_df['totalCurrentLiabilities']

##EFFICIENCY##
efficiency_df = pd.DataFrame()
efficiency_df['assetTurnover'] = refined_df['totalRevenue']/refined_df['totalAssets']
efficiency_df['inventoryTurnover'] = refined_df['totalRevenue']/refined_df['inventory']
efficiency_df['receivablesTurnover'] = refined_df['totalRevenue']/refined_df['currentNetReceivables']

##DEBT & INTEREST##
debt_interest_df = pd.DataFrame()
debt_interest_df['interestCoverage'] = refined_df['interestExpense']/refined_df['ebit']
debt_interest_df['debtToCap'] = refined_df['longTermDebt']/(refined_df['totalShareholderEquity'] + refined_df['longTermDebt'])
debt_interest_df['debtToAssets'] = (refined_df['shortTermDebt'] + refined_df['longTermDebt']) / refined_df['totalAssets']

#Export dataframes to csvs
# refined_df.to_csv('final_dataset.csv', encoding='utf-8', index=False)

stock_eval_df.to_csv('stock_evaluation.csv', encoding='utf-8', index=False)
# profit_df.to_csv('profitability.csv', encoding='utf-8', index=False)
# fin_cond_df.to_csv('financial_condition.csv', encoding='utf-8', index=False)
# efficiency_df.to_csv('efficiency.csv', encoding='utf-8', index=False)
# debt_interest_df.to_csv('debt_and_interest.csv', encoding='utf-8', index=False)