import pandas as pd
import numpy as np
import yfinance as yf
import talib as ta
import time
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order

# Step 1: Define IB API Client Class
class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print(f"Error {reqId} - {errorCode}: {errorString}")

    def nextValidId(self, orderId):
        self.nextOrderId = orderId

# Step 2: Connect to TWS
def connect_to_tws():
    app = IBApi()
    app.connect("127.0.0.1", 7497, clientId=1)  # 7497 is TWS paper trading port
    app.nextOrderId = None

    # Start the client in a separate thread
    app_thread = Thread(target=app.run)
    app_thread.start()

    # Wait for connection
    while app.nextOrderId is None:
        time.sleep(0.1)
    return app

# Step 3: Define Stock Contract (AAPL)
def create_contract(symbol):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.currency = "USD"
    contract.exchange = "SMART"
    return contract

# Step 4: Define Order Function
def create_order(action, quantity):
    order = Order()
    order.action = action  # "BUY" or "SELL"
    order.orderType = "MKT"
    order.totalQuantity = quantity
    order.transmit = True
    return order

# Step 5: Download Historical Data and Calculate Indicators
df = yf.download('AAPL', start='2022-01-01', end='2023-10-01')
df['ATR'] = ta.ATR(df['High'], df['Low'], df['Close'], timeperiod=14)
atr_threshold = 1.5

df['Upper_Threshold'] = df['Close'] + (df['ATR'] * atr_threshold)
df['Lower_Threshold'] = df['Close'] - (df['ATR'] * atr_threshold)
df['Buy_Signal'] = np.where(df['Close'] > df['Upper_Threshold'], 1, 0)
df['Sell_Signal'] = np.where(df['Close'] < df['Lower_Threshold'], -1, 0)

# Step 6: Place Orders Based on Signals
def trade_strategy(app):
    quantity = 10  # Define the order quantity
    symbol = "AAPL"
    contract = create_contract(symbol)

    for i in range(1, len(df)):
        if df['Buy_Signal'][i] == 1 and df['Buy_Signal'][i - 1] == 0:
            print(f"Placing Buy Order for {symbol}")
            order = create_order("BUY", quantity)
            app.placeOrder(app.nextOrderId, contract, order)
            app.nextOrderId += 1

        elif df['Sell_Signal'][i] == -1 and df['Sell_Signal'][i - 1] == 0:
            print(f"Placing Sell Order for {symbol}")
            order = create_order("SELL", quantity)
            app.placeOrder(app.nextOrderId, contract, order)
            app.nextOrderId += 1

# Step 7: Run the Strategy
if __name__ == "__main__":
    app = connect_to_tws()
    try:
        trade_strategy(app)
    finally:
        app.disconnect()
