import streamlit as st
import yfinance as yf
import openai

# Set your OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# App title
st.title("📈 AI-Powered Stock Insights")

# User input for stock ticker
ticker = st.text_input("Enter a stock ticker (e.g., AAPL, MSFT, GOOGL):")

# If ticker entered, fetch and display data
if ticker:
    try:
        # Get stock data
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        
        if hist.empty:
            st.warning("No historical data found for this ticker.")
        else:
            st.subheader(f"{ticker.upper()} - Last 1 Month Closing Prices")
            st.line_chart(hist["Close"])

            # Ask OpenAI for insight
            with st.spinner("Analyzing with AI..."):
                prompt = (
                    f"You're a financial analyst. Analyze recent trends in the stock price "
                    f"of {ticker.upper()} over the past month based on general market behavior. "
                    f"What might explain the movement, and what should an investor consider next?"
                )

                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful financial analyst."},
                        {"role": "user", "content": prompt}
                    ]
                )

                st.subheader("🤖 AI Insight")
                st.write(response.choices[0].message.content)

    except Exception as e:
        st.error(f"Error loading {ticker.upper()}: {e}")
