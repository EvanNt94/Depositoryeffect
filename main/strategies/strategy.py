import pandas as pd
from config.Parameter import Parameter
from stockexchange.fetch_stock.StockFetcher import StockFetcher


class Strategy:
    def __init__(self):
        self.strategy_name = None
        self.outstanding_shares = None
        self.parameter = None

    def set_parameter(self, parameter: Parameter):
        self.parameter = parameter

    def set_StockFetcher(self, stockFetcher: StockFetcher):
        self.stockFetcher = stockFetcher

    def generate_signals(self) -> pd.DataFrame:
        raise NotImplementedError(
            "Bitte generate_signals() in Subklasse implementieren."
        )

    def remove_nan_values(Self, df: pd.DataFrame) -> pd.DataFrame:
        # Remove all rows with any NaN values
        df_clean = df.dropna()
        return df_clean

    def sort_stocks(self, start_date, df):
        print("in sort stocks")

    def sort_df(self, df):
        pass

    def set_outstanding_shares(self, outstanding_shares):
        self.outstanding_shares = outstanding_shares
