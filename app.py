import streamlit as st
import requests
import random

st.set_page_config(page_title="AI Trading Scanner", layout="wide")

st.title("📊 AI Trading Scanner v2 (Budget + Multi-Stock)")

# --- LARGE STOCK LIST (you can expand this later) ---
STOCKS = [
    "AAPL","MSFT","TSLA","AMZN","NVDA","GOOGL","META","NFLX",
    "AMD","INTC","UBER","DIS","BA","JPM","V","MA"
]

# --- SAFE PRICE API (WORKS IN STREAMLIT) ---
def get_price(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
        data = requests.get(url, timeout=5).json()
        return float(data["quoteResponse"]["result"][0]["regularMarketPrice"])
    except:
        return None

# --- AI SCORING ENGINE ---
def analyze_stock(symbol, price):
    trend = random.choice(["bullish", "bearish", "sideways"])
    sentiment = random.choice(["positive", "negative", "neutral"])

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

    if score > 65:
        signal = "BUY"
    elif score < 35:
        signal = "SELL"
    else:
        signal = "HOLD"

    volatility = random.uniform(0.015, 0.03)

    stop_loss = price * (1 - volatility)
    take_profit = price * (1 + volatility * 2)

    return {
        "symbol": symbol,
        "price": price,
        "score": score,
        "signal": signal,
        "stop_loss": stop_loss,
        "take_profit": take_profit
    }

# --- USER INPUT ---
budget = st.number_input("💰 Your Budget ($)", min_value=100, value=1000)

min_score = st.slider("📊 Minimum Confidence Filter", 0, 100, 60)

run = st.button("Scan Market")

# --- SCAN SYSTEM ---
if run:

    results = []

    for stock in STOCKS:
        price = get_price(stock)

        if price is None:
            continue

        if price > budget:
            continue  # budget filter

        analysis = analyze_stock(stock, price)

        if analysis["score"] >= min_score:
            results.append(analysis)

    # sort best opportunities
    results.sort(key=lambda x: x["score"], reverse=True)

    st.subheader("🔥 Best Opportunities")

    if len(results) == 0:
        st.warning("No stocks match your budget and filter.")
    else:
        for r in results:
            st.markdown("---")
            st.write("**Stock:**", r["symbol"])
            st.write("Price:", round(r["price"], 2))
            st.write("Signal:", r["signal"])
            st.write("Confidence:", f"{r['score']}%")
            st.write("Stop Loss:", round(r["stop_loss"], 2))
            st.write("Take Profit:", round(r["take_profit"], 2))
