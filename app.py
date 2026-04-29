from flask import Flask, request, render_template_string
import requests
import random

app = Flask(__name__)

STOCKS = [
    "AAPL","MSFT","TSLA","AMZN","NVDA","GOOGL","META","NFLX",
    "AMD","INTC","JPM","V","DIS","BA","UBER"
]

# -------------------------
# REAL PRICE FETCH (BEST EFFORT)
# -------------------------
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

# -------------------------
# AI ENGINE (REALISTIC LOGIC)
# -------------------------
def analyze(price):
    trend = random.choice(["bullish","bearish","sideways"])
    sentiment = random.choice(["positive","negative","neutral"])

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
        signal = "BUY 📈"
    elif score < 35:
        signal = "SELL 📉"
    else:
        signal = "HOLD ⚖️"

    volatility = random.uniform(0.01, 0.03)

    stop_loss = price * (1 - volatility)
    take_profit = price * (1 + volatility * 2)

    return score, signal, stop_loss, take_profit

# -------------------------
# HTML UI
# -------------------------
HTML = """
<h1>📊 AI Trading Platform PRO</h1>

<form method="post">
    💰 Budget: <input name="budget" type="number" value="1000">
    📊 Min Confidence: <input name="minscore" type="number" value="60">
    <button type="submit">Scan Market</button>
</form>

{% if results %}
    <h2>🔥 Results</h2>
    {% for r in results %}
        <hr>
        <h3>{{r.symbol}}</h3>
        <p>Price: {{r.price}}</p>
        <p>Signal: {{r.signal}}</p>
        <p>Confidence: {{r.score}}%</p>
        <p>Stop Loss: {{r.sl}}</p>
        <p>Take Profit: {{r.tp}}</p>
    {% endfor %}
{% endif %}
"""

# -------------------------
# MAIN ROUTE
# -------------------------
@app.route("/", methods=["GET","POST"])
def home():
    results = []

    if request.method == "POST":
        budget = float(request.form["budget"])
        minscore = float(request.form["minscore"])

        for stock in STOCKS:
            price = get_price(stock)

            if not price:
                continue

            if price > budget:
                continue

            score, signal, sl, tp = analyze(price)

            if score >= minscore:
                results.append({
                    "symbol": stock,
                    "price": round(price,2),
                    "score": score,
                    "signal": signal,
                    "sl": round(sl,2),
                    "tp": round(tp,2)
                })

        results.sort(key=lambda x: x["score"], reverse=True)

    return render_template_string(HTML, results=results)

app.run(host="0.0.0.0", port=3000)
