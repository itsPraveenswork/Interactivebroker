from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from decimal import Decimal

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        # Define the contract (AAPL stock on SMART exchange)
        mycontract = Contract()
        mycontract.symbol = "TSLA"
        mycontract.secType = "STK"
        mycontract.exchange = "SMART"
        mycontract.currency = "USD"

        # Request contract details (optional)
        self.reqContractDetails(orderId, mycontract)

    def contractDetails(self, reqId: int, contractDetails):
        print(contractDetails.contract)

        # Define the order
        myorder = Order()
        myorder.orderId = reqId
        myorder.action = "BUY"  # Buy or Sell
        myorder.orderType = "MKT"  # Limit order
        # myorder.lmtPrice = 227.00  # Limit price
        myorder.totalQuantity = 1  # Quantity of stock to sell
        myorder.tif = "GTC"  # Good-Til-Canceled
        myorder.eTradeOnly = ''
        myorder.firmQuoteOnly = ''
        # Place the order
        self.placeOrder(myorder.orderId, contractDetails.contract, myorder)
       

    def openOrder(self, orderId: int, contract: Contract, order: Order, orderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}")

    def orderStatus(self, orderId: int, status: str, filled: Decimal, remaining: Decimal, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print(f"orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}")

    def execDetails(self, reqId: int, contract: Contract, execution):
        print(f"reqId: {reqId}, contract: {contract}, execution: {execution}")

app = TestApp()
app.connect("127.0.0.1", 7497, 112)  # Ensure correct Client ID and port for live or paper trading
app.run()

