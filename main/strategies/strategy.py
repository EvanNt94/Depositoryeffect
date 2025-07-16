import pandas as pd
from stockexchange.fetch_stock.StockFetcher import StockFetcher


class Strategy:
    def __init__(self):
        self.strategy_name = None
        self.outstanding_shares = None

    def set_StockFetcher(self, stockFetcher: StockFetcher):
        self.stockFetcher = stockFetcher

    def generate_signals(self) -> pd.DataFrame:
        raise NotImplementedError(
            "Bitte generate_signals() in Subklasse implementieren."
        )

    def sort_stocks(self, start_date, df):
        print("in sort stocks")

    def sort_df(self, df):
        pass

    def set_outstanding_shares(self, outstanding_shares):
        self.outstanding_shares = outstanding_shares
