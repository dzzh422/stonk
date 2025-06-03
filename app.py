import streamlit as st
import yfinance as yf

st.title("Simple Stock Tracker")

ticker = st.text_input("Enter stock ticker (e.g., AAPL)")

if ticker:
    data = yf.download(ticker, period="5d", interval="1d")
    st.write(f"Showing data for {ticker}")
    st.line_chart(data["Close"])
