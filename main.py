import streamlit as st
import yfinance as yf
import os
import numpy as np
import pandas as pd
import requests
from datetime import datetime

todays_date = datetime.today().strftime('%Y-%m-%d')

url = 'http://data.fixer.io/api/'
ACCESS_KEY = os.environ.get('FIXER_API_KEY') 

@st.cache
def make_request(url):
    '''
    Makes request to the fixer.io/api.
    the TYPE variable defines if a latest or a historic currency rate will be requested
    '''
    #data = {}
    try:
        url_request = ''.join([url, 'latest', '?access_key=', ACCESS_KEY])
        print('hello world')
        # measuring time in order to make a requests every 10 secs (since i am using the free key, i have limited amount of requests)
        data = requests.get(url_request).json()
        rates = pd.DataFrame(data)
        rates = rates.drop(columns=['success', 'base','timestamp'])
        rates = rates.rename(columns={'date':'Date', 'rates':'Rate'})
    except Exception as e:
        print(e)
    return rates.loc[['USD','GBP','CHF','DKK','JPY','SGD']]

@st.cache
def get_stock_data(inputs):
    tickerData = yf.Ticker(stock_ticker)
    tickerDf = tickerData.history(period='1d', start=inputs[0] , end=inputs[1])
    return tickerDf

### WEB APP ###

## UPPER ##
st.write(todays_date)
st.title("Finance App")
st.write("""
## Top Stocks and Currencies from all over the world
""")

## SIDE BAR ##
st.sidebar.header('User Input Parameters')
st.sidebar.write('Stocks')

    # user inputs #
stock_ticker = st.sidebar.selectbox("Select stock", ("KO","TSLA","HPE","AMAT"))

start_date = st.sidebar.slider('Start Date', datetime(2015, 1, 1), datetime(2021, 1, 1), value = datetime(2018, 1, 1))
final_date = st.sidebar.slider('Final Date', datetime(2015, 1, 1), datetime(2021, 1, 15), value = datetime(2021, 1, 1))
start_date = start_date.strftime('%Y-%m-%d')
final_date = final_date.strftime('%Y-%m-%d')
inputs = [start_date, final_date]

st.write("**Major currencies (EURO BASE)**")
st.write(make_request(url))

tickerDf = get_stock_data(inputs)
st.write(f"**{stock_ticker} - Close**")
st.write(f"From: {inputs[0]}  To: {inputs[1]}")
st.line_chart(tickerDf.Close)
st.write(f"**{stock_ticker} - Open**")
st.line_chart(tickerDf.Volume)










