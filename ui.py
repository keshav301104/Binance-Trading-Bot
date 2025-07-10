import streamlit as st
from binance.client import Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Connect to Binance Futures Testnet
client = Client(API_KEY, API_SECRET, testnet=True)

# --- Streamlit UI ---
st.set_page_config(page_title="Binance Trading Bot", layout="centered")
st.title("🤖 Binance Futures Trading Bot (Testnet)")

# Symbol & Side
symbol = st.selectbox("Symbol", ["BTCUSDT"])
side = st.selectbox("Order Side", ["BUY", "SELL"])
order_type = st.radio("Order Type", ["Market", "Limit", "Stop-Limit"])
quantity = st.number_input("Quantity (e.g., 0.01)", min_value=0.001, step=0.001, format="%.3f")

price = None
stop_price = None

if order_type == "Limit":
    price = st.number_input("Limit Price", min_value=0.0)
elif order_type == "Stop-Limit":
    stop_price = st.number_input("Stop Price", min_value=0.0)
    price = st.number_input("Limit Price (after stop triggers)", min_value=0.0)

# Submit Order
if st.button("📩 Place Order"):
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
        st.success("✅ Order placed successfully")
        st.json(order)
    except Exception as e:
        st.error(f"❌ Error: {e}")
