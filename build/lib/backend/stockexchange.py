'''
We put some classes here to handle the stock exchange.
maybe something with api and such.

theory:

- first we do the tickers
- then we do the notebooks:
    - SX/price
    - SX/info
    - SX/market/sector
    - sx/data
    ... these will initialize the data
- then we do the api
- then we do the worker implementations

'''

from datetime import datetime
from typing import List
from tradx.backend.stock import StockPrice

class StockExchange:
    def __init__(self, name: str):
        self.name = name
        self.timezone = None

    def get_stock_price(self, stock_symbol: str) -> float:
        pass
    
    def get_stock_history(self, stock_symbol: str, start_date: datetime, end_date: datetime) -> List[StockPrice]:
        pass
