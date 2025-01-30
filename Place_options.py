from ib_insync import *
import time

# Connect to Interactive Brokers
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=108) # Port 7497 is usually for TWS; 4002 is for Gateway

# Define the option contract details
contract = Option(
    symbol='AAPL',          # Underlying stock symbol, e.g., 'AAPL'
    lastTradeDateOrContractMonth='20241108',  # Expiration date of option (YYYYMMDD)
    strike=250.37,             # Strike price
    right='C',              # 'C' for Call, 'P' for Put
    exchange= 'SMART' # Use 'SMART' for automatic routing
)

# Define the order details
order = MarketOrder('BUY', 1)  # 'BUY' or 'SELL' and the quantity of contracts

# Place the order
trade = ib.placeOrder(contract, order)
print(f"Order placed: {trade}")

# Wait until the order fills
ib.sleep(1)
while trade.orderStatus.status != 'Filled':
    ib.sleep(1)
    print(f"Order status: {trade.orderStatus.status}")

# Disconnect
ib.disconnect()
