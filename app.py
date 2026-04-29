import streamlit as st
import requests
import random

st.set_page_config(page_title="AI Trading Platform", layout="wide")

st.title("📊 AI Trading Platform (Pro Version)")

# -----------------------------
# STOCK UNIVERSE
# -----------------------------
STOCKS = [
    "AAPL","MSFT","TSLA","AMZN","NVDA","GOOGL","META","NFLX",
    "AMD","INTC","JPM","V","MA","DIS","BA","UBER"
]

# -----------------------------
# PRICE FETCH (SAFE)
# -----------------------------
def get_price(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
        data = requests.get(url, timeout=5).json()
        result = data["quoteResponse"]["result"]
        if not result:
            return None
        return float(result[0]["regularMarketPrice"])
    except:
        return None

# -----------------------------
# AI ENGINE
# -----------------------------
def analyze(symbol, price):
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

    volatility = random.uniform(0.01, 0.03)

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

# -----------------------------
# UI CONTROLS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    budget = st.number_input("💰 Budget ($)", min_value=100, value=1000)

with col2:
    min_score = st.slider("📊 Min Confidence", 0, 100, 60)

run = st.button("🚀 Scan Market")

# -----------------------------
# RESULTS
# -----------------------------
if run:

    results = []

    progress = st.progress(0)

    for i, stock in enumerate(STOCKS):

        price = get_price(stock)

        if price is None:
            continue

        # FIXED BUDGET LOGIC (IMPORTANT)
        if price > budget:
            continue

        result = analyze(stock, price)

        if result["score"] >= min_score:
            results.append(result)

        progress.progress((i + 1) / len(STOCKS))

    results.sort(key=lambda x: x["score"], reverse=True)

    st.subheader("🔥 Best Opportunities")

    if not results:
        st.warning("No matches found. Try increasing budget or lowering filter.")
    else:
        for r in results:
            st.markdown("---")
            st.write("📌 Stock:", r["symbol"])
            st.write("💵 Price:", round(r["price"], 2))
            st.write("📊 Signal:", r["signal"])
            st.write("🧠 Confidence:", f"{r['score']}%")
            st.write("🛑 Stop Loss:", round(r["stop_loss"], 2))
            st.write("🎯 Take Profit:", round(r["take_profit"], 2))
