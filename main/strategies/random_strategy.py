from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from strategies.strategy import Strategy


class RandomStrategy(Strategy):

    def __init__(self):
        super().__init__()
        self.momentum_days = 30
        self.strategy_name = "Random"

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

        concatiniert_ergebnis["Random"] = np.random.rand(len(concatiniert_ergebnis))
        concatiniert_ergebnis = self.remove_nan_values(concatiniert_ergebnis)
        concatiniert_ergebnis = concatiniert_ergebnis.sort_values(
            by="Random", ascending=False
        )

        # Anhängen
        # concatiniert_ergebnis = pd.concat([concatiniert_ergebnis, new_row])

        concatiniert_ergebnis.name = "Momentum: " + list(df.index)[pos].strftime(
            "%Y-%m-%d"
        )

        concatiniert_ergebnis = concatiniert_ergebnis.sort_values(
            by="Random", ascending=False
        )

        return concatiniert_ergebnis

    def sort_df(self, df):
        return df.sort_values(by="Random", ascending=False).copy()
