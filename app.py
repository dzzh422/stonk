import streamlit as st
import yfinance as yf
import openai
import os

# Get your OpenAI key (store as a Streamlit secret or manually input it)
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("📈 AI Stock Insights")

# Input: list of tickers
tickers = st.text_input("Enter stock tickers (comma-separated):", "AAPL,MSFT,TSLA")

if tickers:
    for symbol in [t.strip().upper() for t in tickers.split(',')]:
        st.subheader(f"🔎 {symbol}")
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="1mo")
            info = stock.info

            st.line_chart(hist["Close"])

            # Show some key stats
            st.write(f"**Current Price**: ${hist['Close'][-1]:.2f}")
            st.write(f"**Market Cap**: {info.get('marketCap', 'N/A')}")
            st.write(f"**P/E Ratio**: {info.get('trailingPE', 'N/A')}")

            # Prepare AI prompt
            prompt = (
                f"Stock ticker: {symbol}\n"
                f"Current price: ${hist['Close'][-1]:.2f}\n"
                f"P/E Ratio: {info.get('trailingPE', 'N/A')}\n"
                f"Market Cap: {info.get('marketCap', 'N/A')}\n"
                f"Based on this information, should I buy, sell, or hold {symbol}? Respond with one recommendation and a short explanation."
            )

            with st.spinner(f"Analyzing {symbol}..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=100,
                )
                ai_response = response.choices[0].message["content"]
                st.success("AI Insight:")
                st.markdown(ai_response)

        except Exception as e:
            st.error(f"Error loading {symbol}: {e}")
