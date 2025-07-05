#!/usr/bin/env python3
import threading
import time
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

class OptionChainApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString, *rest):
        print(f"Error: {reqId} | {errorCode} | {errorString}, {rest}")

    def contractDetails(self, reqId: int, contractDetails):
        # Ausgabe jedes gefundenen Optionskontrakts
        contract = contractDetails.contract
        print(f"Option: Symbol={contract.symbol}, SecType={contract.secType}, "
              f"Expiry={contract.lastTradeDateOrContractMonth}, Strike={contract.strike}, "
              f"Right={contract.right}, Exchange={contract.exchange}")

    def contractDetailsEnd(self, reqId: int):
        print(f"Ende der Optionen für ReqId: {reqId}")
        self.disconnect()

def main():
    app = OptionChainApp()
    app.connect("127.0.0.1", 7497, clientId=123)

    # Starte den Netzwerk-Thread
    thread = threading.Thread(target=app.run, daemon=True)
    thread.start()

    # Warten, bis die Verbindung steht
    time.sleep(1)

    # Erstelle ein "unvollständiges" Options-Contract für AAPL
    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "OPT"
    contract.exchange = "SMART"
    contract.currency = "USD"
    # lastTradeDateOrContractMonth, strike, right usw. bleiben leer,
    # um den gesamten Optionskatalog zurückzugeben

    reqId = 1
    app.reqContractDetails(reqId, contract)

    thread.join()

if __name__ == '__main__':
    main()