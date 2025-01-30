from ib_insync import *

# Connect to Interactive Brokers
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)  # Adjust port and clientId as needed

# Define the option contract details
contract = Option(
    symbol='AAPL',          # Underlying stock symbol
    lastTradeDateOrContractMonth='20241115',  # Expiration date (YYYYMMDD)
    strike=250,             # Strike price
    right='C',              # 'C' for Call, 'P' for Put
    exchange='SMART'        # SMART routing
)

# Request contract details to ensure the contract exists
contracts = ib.reqContractDetails(contract)
if not contracts:
    print("Contract not found. Please verify the contract details.")
else:
    # Define the order details
    order = MarketOrder('BUY', 1)  # 'BUY' or 'SELL' and the quantity of contracts

    # Place the order
    trade = ib.placeOrder(contract, order)
    print(f"Order placed: {trade}")

    # Wait until the order fills
    while not trade.isDone():
        ib.waitOnUpdate()
        print(f"Order status: {trade.orderStatus.status}")

# Disconnect
ib.disconnect()

#basic code to place orders
