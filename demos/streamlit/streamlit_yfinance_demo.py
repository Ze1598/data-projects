# >> streamlit run streamlit_yfinance_demo.py
import yfinance as yf
import streamlit as st
import datetime 

TODAY = datetime.datetime.today()

st.write("""
# Stock Price App

This app shows the open and close values for the stock of a chosen company, using Yahoo Finance data.
""")

st.subheader("Choose the company you want to research")
ticker_symbol = st.text_input("Enter the company symbol", "")
# Create a Ticker for the input symbol
ticker_data = yf.Ticker(ticker_symbol)

# Choose the date range for whcih to get data for, using calendar inputs
st.subheader("Please choose the date interval to get data for")
date_start = st.date_input("Start date", TODAY)
date_end = st.date_input("End date", TODAY)

# Get the data
try:
	st.subheader(f"Fetching daily data for {ticker_symbol} in the period of {date_start} to {date_end}")
	# Use the API to fetch the data
	data = ticker_data.history(period="1d", start=str(date_start), end=str(date_end))
	# Show the dataframe
	st.write(data)
	
	st.subheader("Plot of daily open values")
	st.line_chart(data["Open"])

	st.subheader("Plot of daily close values")
	st.line_chart(data["Close"])

except:
	st.write("There was a problem fetching the data...")