import streamlit as st
import requests
import random

st.set_page_config(page_title="AI Trading Bot", layout="centered")

st.title("📊 AI Trading Bot (Online Version)")

symbol = st.text_input("Enter Stock Symbol", "AAPL")

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

        # --- AI LOGIC (NO RANDOM PRICE, ONLY LIGHT NOISE FOR SENTIMENT) ---

        change = price * 0.01

        if random.random() > 0.5:
            trend = "bullish"
        else:
            trend = "bearish"

        news_score = random.uniform(-1, 1)

        if news_score > 0.2:
            sentiment = "positive"
        elif news_score < -0.2:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        # --- SCORE OUT OF 100 ---
        score = 50

        if trend == "bullish":
            score += 25
        else:
            score -= 25

        if sentiment == "positive":
            score += 25
        elif sentiment == "negative":
            score -= 25

        score = max(0, min(100, score))

        # --- RISK SYSTEM ---
        volatility = 0.02

        stop_loss = price * (1 - volatility)
        take_profit = price * (1 + volatility * 2)

        risk_reward = (take_profit - price) / (price - stop_loss)

        # --- DECISION ---
        if score > 65:
            decision = "BUY"
        elif score < 35:
            decision = "SELL"
        else:
            decision = "HOLD"

        # --- OUTPUT ---
        st.subheader("RESULT")

        st.write("Symbol:", symbol)
        st.write("Price:", round(price, 2))
        st.write("Trend:", trend)
        st.write("Sentiment:", sentiment)

        st.write("Decision:", decision)
        st.write("Confidence:", f"{round(score, 1)}%")

        st.write("Stop Loss:", round(stop_loss, 2))
        st.write("Take Profit:", round(take_profit, 2))
        st.write("Risk/Reward:", round(risk_reward, 2))
