from datetime import datetime, timedelta

import pandas as pd
from strategies.strategy import Strategy


class GrowthStrategy(Strategy):

    def __init__(self):
        super().__init__()
        self.momentum_days = 30
        self.strategy_name = "Growth"

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

        year = df.index[pos].year
        result = {
            ticker: yearly_values.get(year + 1, 0)
            / yearly_values.get(year, 1)  # oder 0, falls Wert fehlt
            for ticker, yearly_values in self.stockFetcher.gewinn.items()
        }
        series = pd.Series(result)
        series.index = pd.MultiIndex.from_product([["Close"], series.index])

        concatiniert_ergebnis["Growth"] = series

        concatiniert_ergebnis = concatiniert_ergebnis.sort_values(
            by="Growth", ascending=False
        )

        # Anhängen
        # concatiniert_ergebnis = pd.concat([concatiniert_ergebnis, new_row])

        concatiniert_ergebnis.name = "Growth: " + list(df.index)[pos].strftime(
            "%Y-%m-%d"
        )

        return concatiniert_ergebnis

    def sort_df(self, df):
        return df.sort_values(by="Growth", ascending=False).copy()
