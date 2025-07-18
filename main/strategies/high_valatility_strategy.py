from datetime import datetime, timedelta

import pandas as pd
from strategies.strategy import Strategy


class HighValatilityStrategy(Strategy):

    def __init__(self):
        super().__init__()
        self.min_volatilty_days = 30
        self.strategy_name = "High-Volatility"

    def sort_stocks(self, actual_pos, df):
        # (Preis heute / Preis vor 30 Tagen) -1
        # Sortieren

        # start_date = start_date_ts.strftime("%Y-%m-%d")
        # print("Sort Stocks Momentum", start_date)

        # print(list(map(lambda i: i.strftime("%Y-%m-%d"), list(df.index))))

        # pos = df.index.get_loc(start_date)
        pos = actual_pos
        close_series_today = df.iloc[pos]
        close_series_span_30d = df.iloc[pos - self.min_volatilty_days : pos + 1]

        ergebnis = close_series_span_30d.std()
        ergebnis_sortiert = ergebnis.sort_values(ascending=False)

        # Concatenaten
        concatiniert_ergebnis = pd.concat(
            [ergebnis_sortiert, close_series_today],
            axis=1,
            keys=["High-Volatility", "Close"],
        )

        concatiniert_ergebnis = self.remove_nan_values(concatiniert_ergebnis)
        concatiniert_ergebnis = concatiniert_ergebnis.sort_values(
            by="High-Volatility", ascending=False
        )

        concatiniert_ergebnis.name = "High-Volatility: " + list(df.index)[pos].strftime(
            "%Y-%m-%d"
        )

        return concatiniert_ergebnis

    def sort_df(self, df):
        return df.sort_values(by="High-Volatility", ascending=False).copy()
