#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
from datetime import datetime

def main():
    st.title("Portfolio out of Nifty50 Stocks")
    
    start_date = st.text_input("Enter the start date (YYYY-MM-DD):")
    end_date = st.text_input("Enter the end date (YYYY-MM-DD):")
    n_days_measure_perf = st.number_input("Enter no. of days to Measure past performance:", value=0, step=1, format="%d")
    top_n_stocks = st.number_input("Enter top N stocks:", value=0, step=1, format="%d")
    in_eq = st.number_input("Enter an Invesment Amount:", value=0, step=1, format="%d")
    
    if st.button("Submit"):
         
        import yfinance as yf
        import pandas as pd

        # Define the NIFTY 50 symbols
        nifty50_symbols = [
            'ADANIENT.NS',
            'ADANIPORTS.NS',
            'APOLLOHOSP.NS',
            'ASIANPAINT.NS',
            'AXISBANK.NS',
            'BAJAJ-AUTO.NS',
            'BAJFINANCE.NS',
            'BAJAJFINSV.NS',
            'BHARTIARTL.NS',
            'BPCL.NS',
            'BRITANNIA.NS',
            'CIPLA.NS',
            'COALINDIA.NS',
            'DIVISLAB.NS',
            'DRREDDY.NS',
            'EICHERMOT.NS',
            'GRASIM.NS',
            'HCLTECH.NS',
            'HDFC.NS',
            'HDFCBANK.NS',
            'HDFCLIFE.NS',
            'HEROMOTOCO.NS',
            'HINDALCO.NS',
            'HINDUNILVR.NS',
            'ICICIBANK.NS',
            'INDUSINDBK.NS',
            'INFY.NS',
            'ITC.NS',
            'JSWSTEEL.NS',
            'KOTAKBANK.NS',
            'LT.NS',
            'M&M.NS',
            'MARUTI.NS',
            'NESTLEIND.NS',
            'NTPC.NS',
            'ONGC.NS',
            'POWERGRID.NS',
            'RELIANCE.NS',
            'SBIN.NS',
            'SBILIFE.NS',
            'SUNPHARMA.NS',
            'TATACONSUM.NS',
            'TATAMOTORS.NS',
            'TATASTEEL.NS',
            'TCS.NS',
            'TECHM.NS',
            'TITAN.NS',
            'ULTRACEMCO.NS',
            'UPL.NS',
            'WIPRO.NS'
        ]


        data = yf.download(nifty50_symbols, start=start_date, end=end_date)

        from datetime import datetime, timedelta

        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        start_date_obj = start_date_obj + timedelta(days=-(1+n_days_measure_perf))
        start_date_obj = start_date_obj.strftime('%Y-%m-%d')

        end_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = end_date_obj + timedelta(days=-1)
        end_date_obj = end_date_obj.strftime('%Y-%m-%d')

        Sample_data = yf.download(nifty50_symbols, start=start_date_obj, end=end_date_obj)


        Sample_data = Sample_data['Close']
        close_prices = data['Close']


        Sample_data = pd.DataFrame(Sample_data)
        close_prices = pd.DataFrame(close_prices)

        Sample_data = Sample_data.reset_index()
        close_prices = close_prices.reset_index()

        close_prices['Amount'] = in_eq/50

        ##
        columns_to_divide = nifty50_symbols

        for index, row in close_prices.iterrows():
            for column in columns_to_divide:
                divided_value = (in_eq/50)/ close_prices[column][0]
                rounded_value = round(divided_value)
                new_column_name = column + '_Quantity'

                close_prices.loc[index, new_column_name] = rounded_value

        ##

        columns_to_multiply = [i+'_Quantity' for i in columns_to_divide]

        for index, row in close_prices.iterrows():
            for i,j in zip(columns_to_divide,columns_to_multiply):
                total_amount = row[i]*row[j]
                new_col_name = i + '_total_amount'
                close_prices.loc[index, new_col_name] = total_amount

        ##        
        columns_to_add = [i+'_total_amount' for i in columns_to_divide]

        close_prices['Equity_Curve'] = 0

        for index, row in close_prices.iterrows():
            total =  sum(row[i] for i in columns_to_add)
            close_prices.at[index,'Equity_Curve'] = total

        close_prices['Equity_Curve'] = close_prices['Equity_Curve'].round()


        ## (Sample Strategy) Past Returns based Selection:

        first_day = Sample_data.iloc[0, 1:]   
        last_day = Sample_data.iloc[-1, 1:]  
        percentage_change = (last_day - first_day) / first_day * 100

        new_table = pd.DataFrame({
            'Columns': columns_to_divide,
            'Value': last_day.values,
            'Percentage Change': percentage_change.values
        })
        new_table = new_table.sort_values('Percentage Change', ascending=False)
        list_top_n = list(new_table.Columns.head(top_n_stocks))
        list_top_n.insert(0,'Date')

        Sample_data_top_n = close_prices[list_top_n]
        Sample_data_top_n['Amount'] = in_eq/top_n_stocks

        ## 
        columns_to_divide_sample = list_top_n[1:]

        for index, row in Sample_data_top_n.iterrows():
            for column in columns_to_divide_sample:
                divided_value = (in_eq/top_n_stocks)/ Sample_data_top_n[column][0]
                rounded_value = round(divided_value)
                new_column_name = column + '_Quantity'

                Sample_data_top_n.loc[index, new_column_name] = rounded_value
        
        ##
        columns_to_multiply_sample = [i+'_Quantity' for i in columns_to_divide_sample]

        for index, row in Sample_data_top_n.iterrows():
            for i,j in zip(columns_to_divide_sample,columns_to_multiply_sample):
                total_amount = row[i]*row[j]
                new_col_name = i + '_total_amount'
                Sample_data_top_n.loc[index, new_col_name] = total_amount
        
        ##
        columns_to_add_sample = [i+'_total_amount' for i in columns_to_divide_sample]

        Sample_data_top_n['Equity_Curve_Sample'] = 0

        for index, row in Sample_data_top_n.iterrows():
            total =  sum(row[i] for i in columns_to_add_sample)
            Sample_data_top_n.at[index,'Equity_Curve_Sample'] = total

        Sample_data_top_n['Equity_Curve_Sample'] = Sample_data_top_n['Equity_Curve_Sample'].round()


        #Sample_data_top_n
        #close_prices
        #columns_to_divide_sample (top stocks)
        #new_table (top stocks performance)
        
        st.markdown(""" ### Past Performance """)
        st.table(new_table.head(10))
        
        ticker_symbol = "^NSEI"
        nifty_data = yf.download(ticker_symbol, start=start_date, end=end_date)
        nifty_data = nifty_data[[ 'Close']]

        nifty_data = pd.DataFrame(nifty_data)
        nifty_data = nifty_data.reset_index()
        nifty_data['Amount'] = in_eq
        nifty_data['Quantity'] = round(in_eq/nifty_data['Close'][0])
        nifty_data['Equity_Curve_Nifty'] = round(nifty_data['Close']*nifty_data['Quantity'])

        ##
        Equity_Curve_Table = pd.merge(close_prices,Sample_data_top_n, on='Date')
        Equity_Curve_Table = pd.merge(Equity_Curve_Table,nifty_data, on='Date')

        Equity_Curve_Table = Equity_Curve_Table[['Date','Equity_Curve','Equity_Curve_Sample','Equity_Curve_Nifty']]

        Equity_Curve_Table['Daily_retruns_Equity_Curve'] = Equity_Curve_Table['Equity_Curve'].pct_change()
        Equity_Curve_Table['Daily_retruns_Equity_Curve_Sample'] = Equity_Curve_Table['Equity_Curve_Sample'].pct_change()
        Equity_Curve_Table['Daily_retruns_Equity_Curve_Nifty'] = Equity_Curve_Table['Equity_Curve_Nifty'].pct_change()

        ## Table of CAGR and other 

        from datetime import datetime

        date1 = datetime.strptime(start_date,'%Y-%m-%d').date()
        date2 = datetime.strptime(end_date,'%Y-%m-%d').date()
        date_diff = (date2 - date1).days
        t = round(date_diff/365,3)

        CAGR_Nifty = round(((((nifty_data['Equity_Curve_Nifty'][len(nifty_data)-1]/nifty_data['Equity_Curve_Nifty'][0])**(1/t))-1) * 100),2)
        CAGR_benchhmark = round(((((close_prices['Equity_Curve'][len(close_prices)-1]/close_prices['Equity_Curve'][0])**(1/t))-1) * 100),2)
        CAGR_Sample = round(((((Sample_data_top_n['Equity_Curve_Sample'][len(Sample_data_top_n)-1]/Sample_data_top_n['Equity_Curve_Sample'][0])**(1/t))-1) * 100),2)

        std_Nifty = Equity_Curve_Table['Daily_retruns_Equity_Curve_Nifty'].std()
        std_benchhmark = Equity_Curve_Table['Daily_retruns_Equity_Curve'].std()
        std_Sample = Equity_Curve_Table['Daily_retruns_Equity_Curve_Sample'].std()

        Volatility_Nifty = round((std_Nifty**(1/252))*100,2)
        Volatility_benchhmark = round((std_benchhmark**(1/252))*100,2)
        Volatility_Sample = round((std_Sample**(1/252))*100,2)

        Sharpe_Ratio_Nifty = round((Equity_Curve_Table['Daily_retruns_Equity_Curve_Nifty'].mean()/std_Nifty)**(1/252),3)
        Sharpe_Ratio_benchhmark = round((Equity_Curve_Table['Daily_retruns_Equity_Curve'].mean()/std_benchhmark)**(1/252),3)
        Sharpe_Ratio_Sample = round((Equity_Curve_Table['Daily_retruns_Equity_Curve_Sample'].mean()/std_Sample)**(1/252),3)

        Sum_Perf = {
            'Index' : ['Nifty Index', 'Benchmark Allocation', 'Sample Strategy'],
            'CAGR %' : [CAGR_Nifty,CAGR_benchhmark,CAGR_Sample],
            'Volatility %' : [Volatility_Nifty,Volatility_benchhmark,Volatility_Sample],
            'Sharpe_Ratio %' : [Sharpe_Ratio_Nifty,Sharpe_Ratio_benchhmark,Sharpe_Ratio_Sample]
        }
        Sum_Perf = pd.DataFrame(Sum_Perf)
        
        st.markdown(""" ### Top Stocks Selected: """)
        st.table(columns_to_divide_sample)
        st.markdown(""" ### Performance Metrics """)
        st.table(Sum_Perf)

        #Sample_data_top_n
        #close_prices
        #columns_to_divide_sample (top stocks)
        #new_table
        #nifty_data
        #Equity_Curve_Table
        #Sum_Perf
        
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()

        ax.plot(Equity_Curve_Table['Date'], Equity_Curve_Table['Equity_Curve_Nifty'], label='Nifty_Index')
        ax.plot(Equity_Curve_Table['Date'], Equity_Curve_Table['Equity_Curve'], label='Benchmark Allocation')
        ax.plot(Equity_Curve_Table['Date'], Equity_Curve_Table['Equity_Curve_Sample'], label='Sample Strategy')

        ax.set_xlabel('Date')
        ax.set_ylabel('Investment')
        ax.set_title('Equity Curves')

        last_date = Equity_Curve_Table['Date'].iloc[-1]
        last_price1 = Equity_Curve_Table['Equity_Curve_Nifty'].iloc[-1]
        last_price2 = Equity_Curve_Table['Equity_Curve'].iloc[-1]
        last_price3 = Equity_Curve_Table['Equity_Curve_Sample'].iloc[-1]

        ax.annotate(f'{last_price1:.2f}', (last_date, last_price1), xytext=(-20, 10), textcoords='offset points')
        ax.annotate(f'{last_price2:.2f}', (last_date, last_price2), xytext=(-20, 10), textcoords='offset points')
        ax.annotate(f'{last_price3:.2f}', (last_date, last_price3), xytext=(-20, 10), textcoords='offset points')

        ax.legend()

        plt.xticks(rotation=45)
        
        st.markdown(""" ### Equity Curve """)
        st.pyplot(plt)
        
        st.text('Rohit Gorle')
        st.text('+91 8446259732')
        st.text('rohitgorle33@gmail.com')
        

if __name__ == "__main__":
    main()


# In[ ]:




