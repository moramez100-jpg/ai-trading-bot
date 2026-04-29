import streamlit as st
import random
import time

st.set_page_config(page_title="AI Trading Bot", layout="centered")

st.title("📊 AI Trading Bot (Stable Online Version)")

symbol = st.text_input("Enter Stock Symbol", "AAPL")

# --- STABLE PRICE SIMULATION (NO API ERRORS) ---
def get_price(symbol):
    base_prices = {
        "AAPL": 190,
        "TSLA": 250,
        "MSFT": 420,
        "AMZN": 180,
        "NVDA": 600
    }

    base = base_prices.get(symbol.upper(), 100)
    
    # small realistic movement
    noise = random.uniform(-2, 2)
    return round(base + noise, 2)

if st.button("Analyze"):

    price = get_price(symbol)

    # --- AI LOGIC (IMPROVED BUT STABLE) ---

    trend = random.choice(["bullish", "bearish", "sideways"])
    sentiment = random.choice(["positive", "negative", "neutral"])

    # SCORE OUT OF 100
    score = 50

    if trend == "bullish":
        score += 25
    elif trend == "bearish":
        score -= 25

    if sentiment == "positive":
        score += 25
    elif sentiment == "negative":
        score -= 25

    score = max(0, min(100, score))

    # --- RISK MANAGEMENT ---
    volatility = random.uniform(0.015, 0.03)

    stop_loss = price * (1 - volatility)
    take_profit = price * (1 + volatility * 2)

    risk_reward = (take_profit - price) / (price - stop_loss)

    # --- DECISION ENGINE ---
    if score > 65:
        decision = "BUY 📈"
    elif score < 35:
        decision = "SELL 📉"
    else:
        decision = "HOLD ⚖️"

    # --- OUTPUT ---
    st.subheader("RESULT")

    st.write("Symbol:", symbol.upper())
    st.write("Price:", price)
    st.write("Trend:", trend)
    st.write("Sentiment:", sentiment)

    st.write("Decision:", decision)
    st.write("Confidence:", f"{score}%")

    st.write("Stop Loss:", round(stop_loss, 2))
    st.write("Take Profit:", round(take_profit, 2))
    st.write("Risk/Reward:", round(risk_reward, 2))
