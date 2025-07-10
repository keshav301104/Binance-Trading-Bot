import os
import typer
import logging
from rich import print
from binance.client import Client
from dotenv import load_dotenv

# Initialize CLI app
cli = typer.Typer()

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Setup logging
if not os.path.exists("logs"):
    os.makedirs("logs")
logging.basicConfig(filename="logs/bot.log", level=logging.INFO)

# Initialize Binance Client
client = Client(API_KEY, API_SECRET, testnet=True)

# ✅ REGISTERED COMMAND
@cli.command()
def market_order(symbol: str, side: str, quantity: float):
    """
    Place a market order on Binance Futures Testnet.
    Example: python bot.py market-order BTCUSDT BUY 0.01
    """
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type="MARKET",
            quantity=quantity
        )
        print(f"[bold green]✅ Order placed successfully:[/bold green] {order}")
        logging.info(f"Market Order: {order}")
    except Exception as e:
        print(f"[bold red]❌ Error placing order:[/bold red] {e}")
        logging.error(f"Error: {e}")

@cli.command("limit-order")
def limit_order(symbol: str, side: str, quantity: float, price: float):
    """
    Place a LIMIT order on Binance Futures Testnet.
    Example:
    python bot.py limit-order BTCUSDT BUY 0.01 58000
    """
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type="LIMIT",
            quantity=quantity,
            price=str(price),
            timeInForce="GTC"
        )
        print(f"[bold cyan]📌 Limit Order placed:[/bold cyan] {order}")
        logging.info(f"Limit Order: {order}")
    except Exception as e:
        print(f"[bold red]❌ Error placing limit order:[/bold red] {e}")
        logging.error(f"Limit Order Error: {e}")

@cli.command("cancel-order")
def cancel_order(symbol: str, order_id: int):
    """
    Cancel an open order by order ID.
    Example: python bot.py cancel-order BTCUSDT 5227059624
    """
    try:
        result = client.futures_cancel_order(symbol=symbol, orderId=order_id)
        print(f"[bold yellow]🛑 Order cancelled:[/bold yellow] {result}")
        logging.info(f"Cancelled Order: {result}")
    except Exception as e:
        print(f"[bold red]❌ Error cancelling order:[/bold red] {e}")
        logging.error(f"Cancel Order Error: {e}")

@cli.command("order-status")
def order_status(symbol: str, order_id: int):
    """
    Check the status of an order.
    Example: python bot.py order-status BTCUSDT 5227059624
    """
    try:
        status = client.futures_get_order(symbol=symbol, orderId=order_id)
        print(f"[bold blue]📦 Order status:[/bold blue] {status}")
        logging.info(f"Order Status: {status}")
    except Exception as e:
        print(f"[bold red]❌ Error fetching order status:[/bold red] {e}")
        logging.error(f"Order Status Error: {e}")

@cli.command("stop-limit-order")
def stop_limit_order(symbol: str, side: str, quantity: float, stop_price: float, limit_price: float):
    """
    Place a Stop-Limit Order on Binance Futures Testnet.
    Example:
    python bot.py stop-limit-order BTCUSDT BUY 0.01 57000 56900
    """
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type="STOP",
            quantity=quantity,
            price=str(limit_price),
            stopPrice=str(stop_price),
            timeInForce="GTC",
            workingType="CONTRACT_PRICE"
        )
        print(f"[bold magenta]🛑 Stop-Limit order placed:[/bold magenta] {order}")
        logging.info(f"Stop-Limit Order: {order}")
    except Exception as e:
        print(f"[bold red]❌ Error placing stop-limit order:[/bold red] {e}")
        logging.error(f"Stop-Limit Error: {e}")


# CLI app entry point
if __name__ == "__main__":
    cli()
