import streamlit as st
import random

st.set_page_config(page_title="AI Trading Bot", layout="centered")

st.title("📊 AI Trading Bot (Simple Version)")

symbol = st.text_input("Enter Stock Symbol", "AAPL")

if st.button("Analyze"):

    # fake price (we will upgrade later)
    price = 100 + random.uniform(-5, 5)

    # simple AI logic
    trend = random.choice(["bullish", "bearish", "sideways"])
    sentiment = random.choice(["positive", "negative", "neutral"])

    score = 0.5

    if trend == "bullish":
        score += 0.2
    if trend == "bearish":
        score -= 0.2

    if sentiment == "positive":
        score += 0.2
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
    st.write("Confidence Score:", round(score, 2))

    st.write("Stop Loss:", round(stop_loss, 2))
    st.write("Take Profit:", round(take_profit, 2))
