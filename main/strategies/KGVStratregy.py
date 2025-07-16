from datetime import datetime, timedelta

import pandas as pd
from strategies.strategy import Strategy


class KGVStrategy(Strategy):

    def __init__(self):
        super().__init__()
        self.momentum_days = 30
        self.strategy_name = "KGV"

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
            ticker: yearly_values.get(year, 0)  # oder 0, falls Wert fehlt
            for ticker, yearly_values in self.stockFetcher.eps.items()
        }
        series = pd.Series(result)
        series.index = pd.MultiIndex.from_product([["Close"], series.index])

        concatiniert_ergebnis["eps"] = series
        concatiniert_ergebnis["KGV"] = (
            concatiniert_ergebnis["Close"] / concatiniert_ergebnis["eps"]
        )

        concatiniert_ergebnis = concatiniert_ergebnis.sort_values(
            by="KGV", ascending=True
        )

        # Anhängen
        # concatiniert_ergebnis = pd.concat([concatiniert_ergebnis, new_row])

        concatiniert_ergebnis.name = "KGV: " + list(df.index)[pos].strftime("%Y-%m-%d")

        return concatiniert_ergebnis

    def sort_df(self, df):
        return df.sort_values(by="KGV", ascending=True).copy()
