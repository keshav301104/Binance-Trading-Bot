# 🤖 Binance Futures Trading Bot (Testnet)

A professional crypto trading bot for the **Binance Futures Testnet**, built using Python with an optional Streamlit-based frontend and full CLI interface.  
Easily place market, limit, and stop-limit orders, manage trades, cancel orders, view open positions, and monitor charts in real-time.

---

![UI Screenshot](https://user-images.githubusercontent.com/your-dashboard-image.png)

---

## 🚀 Features

### ⚙️ Core Trading Bot
- ✅ Market & Limit orders
- ✅ Stop-Limit order support
- ✅ Cancel open orders
- ✅ Order status checker
- ✅ Command-line interface using `Typer`
- ✅ Logging of all trades & errors

### 🌐 Streamlit Frontend UI
- 🔘 Place Market / Limit / Stop-Limit orders via browser
- 🗂 View open and filled orders
- 📉 Live candlestick chart (Plotly + Binance)
- 🔐 Secure API handling using `.env` or Streamlit secrets

---

## 🧱 Project Structure

```bash
binance_trading_bot/
├── advanced_ui.py         # 🔘 Streamlit UI
├── bot.py                 # ⚙️ CLI interface
├── requirements.txt       # 📦 Required libraries
├── .env.example           # 🔐 Env template (safe to push)
├── .gitignore             # 🛡️ Ignores .env & __pycache__
├── README.md              # 📄 Project documentation
├── logs/                  # 📁 (Optional) log directory
