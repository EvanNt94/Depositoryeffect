'''
Here we put some classes to handle the stock.
'''

from datetime import datetime
from typing import List


class StockPrice:
    def __init__(self, date: datetime, price: float):
        self.date = date
        self.price = price

class Stock:
    def __init__(self, symbol: str, name: str):
        self.symbol = symbol
        self.name = name

    def get_price(self, date: datetime) -> StockPrice:
        pass
    
    def get_history(self, start_date: datetime, end_date: datetime) -> List[StockPrice]:
        pass