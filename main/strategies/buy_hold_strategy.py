from datetime import datetime, timedelta

import pandas as pd
from strategies.strategy import Strategy


class BuyHoldStrategy(Strategy):

    def __init__(self):
        super().__init__()
        self.momentum_days = 30
        self.strategy_name = "Buy and hold"

    def sort_stocks(self, actual_pos, df):
        # (Preis heute / Preis vor 30 Tagen) -1
        # Sortieren

        # start_date = start_date_ts.strftime("%Y-%m-%d")
        # print("Sort Stocks Momentum", start_date)

        # print(list(map(lambda i: i.strftime("%Y-%m-%d"), list(df.index))))

        # pos = df.index.get_loc(start_date)
        pos = actual_pos
        close_series_today = df.iloc[pos]

        # Concatenaten
        concatiniert_ergebnis = pd.concat(
            [close_series_today],
            axis=1,
            keys=["Close"],
        )

        outstanding_shares = self.outstanding_shares.copy()
        outstanding_shares.index = pd.MultiIndex.from_product(
            [["Close"], outstanding_shares.index]
        )
        concatiniert_ergebnis["Outstanding Shares"] = outstanding_shares
        concatiniert_ergebnis["Market Cap"] = (
            concatiniert_ergebnis["Close"] * concatiniert_ergebnis["Outstanding Shares"]
        )

        concatiniert_ergebnis = concatiniert_ergebnis.sort_values(
            by="Market Cap", ascending=False
        )

        concatiniert_ergebnis.name = "Market Cap: " + list(df.index)[pos].strftime(
            "%Y-%m-%d"
        )

        return concatiniert_ergebnis

    def sort_df(self, df):
        return df.sort_values(by="Market Cap", ascending=False).copy()
