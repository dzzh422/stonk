import streamlit as st
import yfinance as yf
from openai import OpenAI

# Set OpenAI API key from secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# App title
st.title("AI Stock Advisor")

# User input for stock symbol
ticker_symbol = st.text_input("Enter stock symbol (e.g. AAPL, MSFT):")

# Fetch and display stock data
if ticker_symbol:
    try:
        stock = yf.Ticker(ticker_symbol)
        hist = stock.history(period="1mo")

        st.subheader(f"{ticker_symbol} - Last Month's Stock Price")
        st.line_chart(hist["Close"])

        # Send stock info to OpenAI for insights
        latest_close = hist["Close"][-1]
        prompt = (
            f"The stock {ticker_symbol} is currently trading at ${latest_close:.2f}. "
            "Based on general market trends and recent performance, what should I consider before buying or selling this stock?"
        )

        with st.spinner("Analyzing with GPT..."):
            response = client.chat.completions.create(
                model="gpt-4",  # or "gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content": "You are a helpful financial assistant, but not a financial advisor."},
                    {"role": "user", "content": prompt}
                ]
            )
            advice = response.choices[0].message.content
            st.subheader("AI Insights")
            st.write(advice)

    except Exception as e:
        st.error(f"Error loading data for {ticker_symbol}: {e}")
