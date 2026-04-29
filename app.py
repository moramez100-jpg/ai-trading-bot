import streamlit as st
import requests
import random
import pandas as pd

st.set_page_config(page_title="AI Trading Platform", layout="wide")

# -----------------------------
# SESSION STATE (WATCHLIST + PORTFOLIO)
# -----------------------------
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}

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
# SIDEBAR NAVIGATION
# -----------------------------
page = st.sidebar.radio("Navigation", ["Dashboard", "Scanner", "Watchlist", "Portfolio"])

# =============================
# DASHBOARD
# =============================
if page == "Dashboard":
    st.title("📊 AI Trading Dashboard")

    st.write("Welcome to your trading system.")

    st.metric("Stocks in Universe", len(STOCKS))
    st.metric("Watchlist Items", len(st.session_state.watchlist))
    st.metric("Portfolio Positions", len(st.session_state.portfolio))

# =============================
# SCANNER
# =============================
elif page == "Scanner":
    st.title("🔍 Market Scanner")

    budget = st.number_input("💰 Budget ($)", min_value=100, value=1000)
    min_score = st.slider("📊 Min Confidence", 0, 100, 60)

    if st.button("Run Scan"):

        results = []

        progress = st.progress(0)

        for i, stock in enumerate(STOCKS):

            price = get_price(stock)
            if price is None:
                continue

            # FIXED BUDGET FILTER
            if price > budget:
                continue

            result = analyze_stock(stock, price)

            if result["score"] >= min_score:
                results.append(result)

            progress.progress((i + 1) / len(STOCKS))

        results.sort(key=lambda x: x["score"], reverse=True)

        st.subheader("🔥 Opportunities")

        if not results:
            st.warning("No matches found.")
        else:
            for r in results:
                st.markdown("---")

                st.write("Stock:", r["symbol"])
                st.write("Price:", round(r["price"], 2))
                st.write("Signal:", r["signal"])
                st.write("Confidence:", f"{r['score']}%")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"➕ Watch {r['symbol']}"):
                        if r["symbol"] not in st.session_state.watchlist:
                            st.session_state.watchlist.append(r["symbol"])

                with col2:
                    qty = st.number_input(f"Buy {r['symbol']} qty", 1, 100, key=r["symbol"])
                    if st.button(f"💰 Add to Portfolio {r['symbol']}"):
                        st.session_state.portfolio[r["symbol"]] = qty

# =============================
# WATCHLIST
# =============================
elif page == "Watchlist":
    st.title("⭐ Watchlist")

    if not st.session_state.watchlist:
        st.info("No stocks in watchlist.")
    else:
        for stock in st.session_state.watchlist:
            price = get_price(stock)
            st.write(stock, "-", price)

# =============================
# PORTFOLIO
# =============================
elif page == "Portfolio":
    st.title("💼 Portfolio Simulator")

    if not st.session_state.portfolio:
        st.info("No positions yet.")
    else:
        total_value = 0

        for stock, qty in st.session_state.portfolio.items():
            price = get_price(stock)

            if price:
                value = price * qty
                total_value += value

                st.write(stock, "Qty:", qty, "Value:", round(value, 2))

        st.subheader(f"Total Portfolio Value: ${round(total_value, 2)}")
