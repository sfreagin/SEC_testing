import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import requests
import os
import time

import streamlit as st
from bokeh.plotting import figure, show
from bokeh.models import Legend
from bokeh.models import NumeralTickFormatter
from bokeh.io import show, output_file

#######################################################################################################################

# first get the current working directory
path = os.getcwd()

# Next create 3 folders in the same directory as this .py file:
#   'Income'
#   'BalanceSheet'
#   'CashFlow'

try:
    os.mkdir(path+'/Income')
    os.mkdir(path+'/BalanceSheet')
    os.mkdir(path+'/CashFlow')
except:
    pass

#######################################################################################################################
# this function pulls Income Statement data from stockrow.com
def income_puller(ticker):
    url=f'https://stockrow.com/api/companies/{ticker}/financials.xlsx?dimension=T&section=Income%20Statement&sort=desc'
    response = requests.get(url)
    with open(os.path.join("Income", f"{ticker}_inc.xlsx"), 'wb') as f:
        f.write(response.content)
    time.sleep(0.25)
    
    ticker_df = pd.read_excel(f'./Income/{ticker}_inc.xlsx').T
    # change the first row to the columns
    ticker_df.columns = ticker_df.iloc[0]
    #remove the first row
    ticker_df = ticker_df.iloc[1:]
    
    return ticker_df

# this function pulls Balance Sheet data from StockRow.com
def balance_puller(ticker):
    url=f'https://stockrow.com/api/companies/{ticker}/financials.xlsx?dimension=Q&section=Balance%20Sheet&sort=desc'
    response = requests.get(url)
    with open(os.path.join("BalanceSheet", f"{ticker}_balance.xlsx"), 'wb') as f:
        f.write(response.content)
    time.sleep(0.25)
    
    ticker_df = pd.read_excel(f'./BalanceSheet/{ticker}_balance.xlsx').T
    # change the first row to the columns
    ticker_df.columns = ticker_df.iloc[0]
    #remove the first row
    ticker_df = ticker_df.iloc[1:]
    
    return ticker_df

# this function pulls Cash Flow statement data from StockRow.com
def cashflow_puller(ticker):
    url=f'https://stockrow.com/api/companies/{ticker}/financials.xlsx?dimension=T&section=Cash%20Flow&sort=desc'
    response = requests.get(url)
    with open(os.path.join("CashFlow", f"{ticker}_cashflow.xlsx"), 'wb') as f:
        f.write(response.content)
    time.sleep(0.25)
    
    ticker_df = pd.read_excel(f'./CashFlow/{ticker}_cashflow.xlsx').T
    # change the first row to the columns
    ticker_df.columns = ticker_df.iloc[0]
    #remove the first row
    ticker_df = ticker_df.iloc[1:]
    
    return ticker_df

################################################################################################################
# this function prompts the user for a ticker input and calls the income_puller() function to return a DataFrame
# same for balance_puller() to return Balance Sheet info
def ticker_input():
    income_df = income_puller(ticker.upper())
    balance_df = balance_puller(ticker.upper())
    cashflow_df = cashflow_puller(ticker.upper())
    return income_df, balance_df, cashflow_df, ticker



################################################################################################################
# streamlit starts here
################################################################################################################

st.title('Southpaw Stockrow Screener')

st.header('Visualizing Public Financial Data')
st.write('This streamlit app shows select financial data from publicly-traded companies')
st.text('(P.S. please ignore the errors below; they go away when you input a ticker)')
#st.write("Please enter a ticker below:")
ticker = st.text_input("Please enter a ticker:")

income_df,balance_df, cashflow_df, ticker = ticker_input()
print(f"Financial data for {ticker.upper()} below:")





################################################################################################################
# INCOME STATEMENT CHART

#note I'm labeling my x- and y-axis as xi and yi, short for x-Income_df and y-Income_df
xi = income_df.index

yi1 = income_df['Revenue']
yi2 = income_df['Gross Profit']
yi3 = income_df['Operating Income']
yi4 = income_df['Net Income Common']


p_inc = figure(title=f'Income Statement data for {ticker.upper()}', x_axis_label='Trailing 12 Months (quarterly)',
			x_axis_type = 'datetime',y_axis_label='USD',plot_width=800,plot_height=400)
p_inc.yaxis.formatter = NumeralTickFormatter(format='($0.00a)')

p_inc.add_layout(Legend(),'right')

p_inc.circle(xi,yi1,line_color='green',size=12,fill_alpha=0.25, legend_label='Revenue')
p_inc.circle(xi,yi2,size=6,fill_alpha=0.25, legend_label='Gross Profit')
p_inc.circle(xi,yi3,color='gold',size=6,fill_alpha=0.75, legend_label= "Operating Income")
p_inc.circle(xi,yi4,color='black',size=9,fill_alpha=0.5, legend_label='Net Income')
p_inc.legend.click_policy = 'hide'

st.bokeh_chart(p_inc)

##########################################################################################################
# BALANCE SHEET CHART
xt = balance_df.index

yt1 = balance_df['Total Assets']
yt2 = balance_df['Total liabilities']
yt3 = balance_df['Total current assets']
yt4 = balance_df['Total current liabilities']
yt5 = balance_df['Cash and Short Term Investments']
yt6 = balance_df['Shareholders Equity (Total)']

pt = figure(title=f'Balance Sheet data for {ticker.upper()}', x_axis_label='Trailing 12 Months (quarterly)',
			x_axis_type='datetime',y_axis_label='USD',plot_width=800,plot_height=400)
pt.add_layout(Legend(),'right')

pt.circle(xt,yt1,color='blue',size=12,fill_alpha=0.5,legend_label='Total Assets')
pt.circle(xt,yt2,color='red',size=12,fill_alpha=0.5, legend_label = 'Total Liabilities')
pt.circle(xt,yt3,color='gold',size=6,fill_alpha=0.5, legend_label='Current Assets')
pt.circle(xt,yt4,color='red',size=6,fill_alpha=0.25, legend_label = 'Current Liabilities')
pt.circle(xt,yt5,color='green',size=6,fill_alpha=0.25, legend_label = 'Cash & Equivalents')
pt.circle(xt,yt6,color='black',size=9,fill_alpha=0.55, legend_label = 'Shareholder Equity')
pt.yaxis.formatter = NumeralTickFormatter(format='($0.00a)')
pt.legend.click_policy = 'hide'

st.bokeh_chart(pt)

##########################################################################################################
# CASH FLOW STATEMENT CHART
xcf = cashflow_df.index

ycf1 = cashflow_df['Operating Cash Flow']
ycf2 = -cashflow_df['Capital expenditures']
ycf3 = cashflow_df['Operating Cash Flow'] + cashflow_df['Capital expenditures']


pcf = figure(title=f'Cash Flow Statement data for {ticker.upper()}', x_axis_label='Trailing 12 Months (quarterly)',
			x_axis_type='datetime',y_axis_label='USD',plot_width=800,plot_height=400)
pcf.add_layout(Legend(),'right')

pcf.circle(xcf,ycf1,color='blue',size=12,fill_alpha=0.5,legend_label='Operating Cash Flow')
pcf.circle(xcf,ycf2,color='red',size=12,fill_alpha=0.5, legend_label = 'CapEx')
pcf.circle(xcf,ycf3,color='black',size=9,fill_alpha=0.5, legend_label='Free Cash Flow')
pcf.yaxis.formatter = NumeralTickFormatter(format='($0.00a)')
pcf.legend.click_policy = 'hide'

st.bokeh_chart(pcf)










#####################################################################################################
# Discounted Cash Flow calculations
#####################################################################################################

# these are the columns we're interested in
inc_columns = ['Revenue','Gross Profit','Operating Income','Income Tax Provision', 'Net Income Common']
bal_columns = ['Total Assets','Total current assets','Total liabilities','Total current liabilities',
               'Shareholders Equity (Total)']#,'Shares (Common)']
cfl_columns = ['Capital expenditures','Operating Cash Flow']#,'Equity Repurchase (Common, Net)','Dividends Paid (Common)']

# this will apply only the columns above to each of our financial statement DataFrames
ticker_inc_df = income_df[inc_columns]
ticker_bal_df = balance_df[bal_columns]
ticker_cfl_df = cashflow_df[cfl_columns]

# this will combine or concatenate our three DataFrames into one
ticker_df = pd.concat([ticker_inc_df,ticker_bal_df,ticker_cfl_df], axis=1)

# defining a new column for FCF
ticker_df['FreeCashFlow'] = ticker_df['Operating Cash Flow'] - ticker_df['Capital expenditures']

#############################
# growth rates
#############################

# 1. averaging all FCF growth rates
fcf_growth_list1 = [((ticker_df['FreeCashFlow'][i] - ticker_df['FreeCashFlow'][i+4]) / ticker_df['FreeCashFlow'][i+4]) 
                   for i in range(0,len(ticker_df['FreeCashFlow'])-4)]
fcf_growth_rate1 = sum(fcf_growth_list1)/len(fcf_growth_list1)
#print(f"Free Cash Flow average 1-yr growth rate: {round(fcf_growth_rate1*100,2)}%")


# 2. calculating all cumulative 1-yr average growths at once
growth_list1 = []
for col in ticker_df.columns:
    try:
        col_growth_list1 = [((ticker_df[col][i] - ticker_df[col][i+4]) / ticker_df[col][i+4]) 
                           for i in range(0,len(ticker_df[col])-4)]
        print(f"Avg growth for {col} is {sum(col_growth_list1)/len(col_growth_list1)}")
        growth_list1.append(sum(col_growth_list1)/len(col_growth_list1))
    except:
        print(f"{col} throws an error")
all_metrics_growth_rate1 = sum(growth_list1)/len(growth_list1) 
#print(f"Avg growth: {all_metrics_growth_rate1}")


# 3. this code sorts the growth rates from low to high, then it removes the top 2 and lowest 2
growth_list1.sort()
normalized_ticker_growth1 = sum(growth_list1[2:-2]) / len(growth_list1[2:-2])
#print(f"The 'normalized' growth rate for (almost all) metrics: {round(normalized_ticker_growth1*100,2)}%")


# 4. this version only considers growth rate starting from t = 0, looking backwards at quarterly data
fcf_growth_list2 = [((1+((ticker_df['FreeCashFlow'][0] - ticker_df['FreeCashFlow'][i+4]) / ticker_df['FreeCashFlow'][i+4]))**(1/(1+i/4))-1) 
                    for i in range(len(ticker_df['FreeCashFlow'])-4)]

fcf_growth_rate2 = sum(fcf_growth_list2)/len(fcf_growth_list2)
#print(f"Free Cash Flow avg growth rate last decade: {round(fcf_growth_rate2*100,2)}%")


# 5. doing the above for all metrics
growth_list2 = []
for col in ticker_df.columns:
    try:
        col_growth_list2 = [((1+((ticker_df[col][0] - ticker_df[col][i+4]) / ticker_df[col][i+4]))**(1/(1+i/4))-1) 
                            for i in range(len(ticker_df[col])-4)]
        print(f"Avg growth for {col} is {sum(col_growth_list2)/len(col_growth_list2)}")
        growth_list2.append(sum(col_growth_list2)/len(col_growth_list2))
    except:
        print(f'{col} throws an error')
all_metrics_growth_rate2 = sum(growth_list2)/len(growth_list2) 
#print(f"Avg growth of all metrics: {all_metrics_growth_rate2}")

# 6. this code sorts the growth rates from low to high, then it removes the top 2 and lowest 2
growth_list2.sort()
normalized_ticker_growth2 = sum(growth_list2[2:-2]) / len(growth_list2[2:-2])
#print(f"The 'normalized' growth rate for (almost all) metrics: {round(normalized_ticker_growth2*100,2)}%")


################################################
# DCF function
################################################

def dcf_maker(ticker_df,growth_rate,discount_rate,years):
    # we start at zero, then incrementally add each subsequent year's FCF
    fcf_over_time = 0
    # our base will be the most recent year's FCF
    fcf_start = ticker_df['FreeCashFlow'][0]

    # covering a range of 10 years
    for i in range(1,years+1):
        fcf_over_time += fcf_start * (1+growth_rate)**i / (1+discount_rate)**i

    print(f"Total FCF: ${round(fcf_over_time/1_000_000_000,1)} billion")
    return fcf_over_time

# putting all our growth rates into a list
all_growth_rates = [fcf_growth_rate1,fcf_growth_rate2,all_metrics_growth_rate1,all_metrics_growth_rate2,
                    normalized_ticker_growth1, normalized_ticker_growth2]

# creating a list of possible discount rates
discount_list = np.linspace(0.01,0.08,20).tolist()

# listing a number of DCF years
year_list = [8,9,10,11,12]

# now it runs the dcf_maker() through every possible iteration of the above lists
# and appends the results to a new list
fcf_values_list = []
for rate in all_growth_rates:
    for discount in discount_list:
        for year in year_list:
            #print(f"Growth rate: {round(rate*100,2)}%, Discount rate: {round(discount*100,2)}%, Years: {year}")
            fcf_values_list.append(dcf_maker(ticker_df,rate,discount,year))

fcf_values_list.sort()

# GIMME THE BOKEH
data = fcf_values_list
hist, edges = np.histogram(data, density=True, bins=50)

p = figure(title=f"Free Cash Flow outcomes for {ticker.upper()}\n(note this FCF distribution is still in beta and NOT RELIABLE)",x_axis_label="Predicted FCF ($USD",
			plot_width=800, plot_height=400)
p.xaxis.formatter = NumeralTickFormatter(format='($0.00a)')
p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], line_color="white")

st.bokeh_chart(p)