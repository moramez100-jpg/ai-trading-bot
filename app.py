import streamlit as st
import requests
import random

st.title("📊 AI Trading Bot (Online Version)")

symbol = st.text_input("Stock Symbol", "AAPL")

# --- REAL PRICE FROM FREE API ---
def get_price(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
        data = requests.get(url).json()
        return data["quoteResponse"]["result"][0]["regularMarketPrice"]
    except:
        return None

if st.button("Analyze"):

    price = get_price(symbol)

    if price is None:
        st.error("Could not fetch price. Try AAPL, TSLA, MSFT")
    else:

        trend = random.choice(["bullish", "bearish"])
        sentiment = random.choice(["positive", "negative", "neutral"])

        score = 0.5

        if trend == "bullish":
            score += 0.2
        if sentiment == "positive":
            score += 0.2
        if trend == "bearish":
            score -= 0.2
        if sentiment == "negative":
            score -= 0.2

        decision = "HOLD"
        if score > 0.65:
            decision = "BUY"
        elif score < 0.35:
            decision = "SELL"

        stop_loss = price * 0.98
        take_profit = price * 1.04

        st.subheader("RESULT")
        st.write("Symbol:", symbol)
        st.write("Price:", round(price, 2))
        st.write("Trend:", trend)
        st.write("Sentiment:", sentiment)
        st.write("Decision:", decision)
        st.write("Confidence:", round(score, 2))
        st.write("Stop Loss:", round(stop_loss, 2))
        st.write("Take Profit:", round(take_profit, 2))
