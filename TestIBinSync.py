from ib_insync import *
import time

# Connect to Interactive Brokers TWS
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=204)  # Make sure the port and clientId are correct

# Define the contract (for example, AAPL stock)
contract = Stock('TSLA', 'SMART', 'USD')

# Create a limit order to buy 1 share of AAPL at a limit price of $150
# order = LimitOrder('BUY', 1, 227.17)

# Define the order
myorder = Order()
#myorder.orderId = 1
myorder.action = "SELL"  # Buy or Sell
myorder.orderType = "MKT"  # Limit order
# myorder.lmtPrice = 227.00  # Limit price
myorder.totalQuantity = 1  # Quantity of stock to sell
# myorder.tif = "GTC"  # Good-Til-Canceled

# Place the order
trade = ib.placeOrder(contract, myorder)

# Wait for order status updates
while not trade.isDone():
    ib.sleep(1)
    print(trade.orderStatus.status)

# Disconnect after the order is placed or filled
ib.disconnect()
