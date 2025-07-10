import streamlit as st
from binance.client import Client
from dotenv import load_dotenv
import pandas as pd
import plotly.graph_objects as go
import requests
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Connect to Binance Futures Testnet
client = Client(API_KEY, API_SECRET, testnet=True)

# --- Page Layout ---
st.set_page_config(page_title="Binance Pro Bot", layout="wide")
st.title("🚀 Binance Futures Trading Bot (Testnet)")
st.caption("Place trades, view charts, and manage orders — all in one place.")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["📥 Place Order", "📊 Price Chart", "📜 Order History"])

# ─────────────────────────────
# 📥 TAB 1: Place Order + Open Orders
# ─────────────────────────────
with tab1:
    col1, col2 = st.columns(2)

    # ─── Order Placement ───
    with col1:
        st.subheader("📥 Place New Order")
        symbol = st.selectbox("Symbol", ["BTCUSDT"])
        side = st.radio("Side", ["BUY", "SELL"], horizontal=True)
        order_type = st.radio("Order Type", ["Market", "Limit", "Stop-Limit"], horizontal=True)
        quantity = st.number_input("Quantity", min_value=0.001, step=0.001, format="%.3f")

        price = None
        stop_price = None

        if order_type == "Limit":
            price = st.number_input("Limit Price", min_value=0.0)
        elif order_type == "Stop-Limit":
            stop_price = st.number_input("Stop Price", min_value=0.0)
            price = st.number_input("Limit Price", min_value=0.0)

        if st.button("✅ Place Order"):
            try:
                if order_type == "Market":
                    order = client.futures_create_order(
                        symbol=symbol,
                        side=side,
                        type="MARKET",
                        quantity=quantity
                    )
                elif order_type == "Limit":
                    order = client.futures_create_order(
                        symbol=symbol,
                        side=side,
                        type="LIMIT",
                        quantity=quantity,
                        price=str(price),
                        timeInForce="GTC"
                    )
                elif order_type == "Stop-Limit":
                    order = client.futures_create_order(
                        symbol=symbol,
                        side=side,
                        type="STOP",
                        quantity=quantity,
                        stopPrice=str(stop_price),
                        price=str(price),
                        timeInForce="GTC",
                        workingType="CONTRACT_PRICE"
                    )
                st.success("✅ Order placed successfully!")
                with st.expander("🧾 Order Response"):
                    st.json(order)
            except Exception as e:
                st.error(f"❌ Error placing order: {e}")

    # ─── Open Orders + Cancel ───
    with col2:
        st.subheader("📂 Open Orders")
        try:
            open_orders = client.futures_get_open_orders(symbol="BTCUSDT")
            if open_orders:
                for order in open_orders:
                    with st.expander(f"🧾 Order ID: {order['orderId']} — {order['side']} {order['origQty']}"):
                        st.json(order)
                        if st.button(f"❌ Cancel Order {order['orderId']}", key=order['orderId']):
                            try:
                                result = client.futures_cancel_order(symbol=order['symbol'], orderId=order['orderId'])
                                st.success(f"✅ Cancelled Order ID: {result['orderId']}")
                            except Exception as ce:
                                st.error(f"❌ Cancel Error: {ce}")
            else:
                st.info("No open orders found.")
        except Exception as e:
            st.error(f"⚠️ Error fetching open orders: {e}")

# ─────────────────────────────
# 📊 TAB 2: Price Chart
# ─────────────────────────────
with tab2:
    st.subheader("📈 Live BTCUSDT Price Chart")

    interval = st.selectbox("Chart Interval", ["1m", "5m", "15m", "1h"], index=1)
    limit = st.slider("Candlestick Count", min_value=10, max_value=100, value=50)

    url = f"https://testnet.binancefuture.com/fapi/v1/klines?symbol=BTCUSDT&interval={interval}&limit={limit}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=["Time", "Open", "High", "Low", "Close", "Volume",
                                         "_", "_", "_", "_", "_", "_"])
        df["Time"] = pd.to_datetime(df["Time"], unit="ms")
        df["Open"] = df["Open"].astype(float)
        df["High"] = df["High"].astype(float)
        df["Low"] = df["Low"].astype(float)
        df["Close"] = df["Close"].astype(float)

        fig = go.Figure(data=[go.Candlestick(
            x=df["Time"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        )])
        fig.update_layout(xaxis_rangeslider_visible=False, height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("❌ Failed to fetch chart data.")

# ─────────────────────────────
# 📜 TAB 3: Order History
# ─────────────────────────────
with tab3:
    st.subheader("📜 Filled Orders (Trade History)")

    try:
        history = client.futures_account_trades(symbol="BTCUSDT")
        if history:
            df = pd.DataFrame(history)
            df["time"] = pd.to_datetime(df["time"], unit="ms")
            df = df[["orderId", "symbol", "side", "qty", "price", "realizedPnl", "time"]]
            st.dataframe(df.sort_values("time", ascending=False), use_container_width=True)
        else:
            st.info("No trade history yet.")
    except Exception as e:
        st.error(f"⚠️ Error fetching trade history: {e}")
