from datetime import datetime, timedelta

import pandas as pd
from strategies.strategy import Strategy


class MomentumStrategy(Strategy):

    def __init__(self):
        super().__init__()
        self.momentum_days = 30
        self.strategy_name = "Momentum"

    def sort_stocks(self, actual_pos, df):
        # (Preis heute / Preis vor 30 Tagen) -1
        # Sortieren

        # start_date = start_date_ts.strftime("%Y-%m-%d")
        # print("Sort Stocks Momentum", start_date)

        # print(list(map(lambda i: i.strftime("%Y-%m-%d"), list(df.index))))

        # pos = df.index.get_loc(start_date)
        pos = actual_pos
        close_series_today = df.iloc[pos]
        close_series_30d = df.iloc[pos - self.momentum_days]

        ergebnis = (close_series_today / close_series_30d) - 1
        ergebnis_sortiert = ergebnis.sort_values(ascending=False)

        # Concatenaten
        concatiniert_ergebnis = pd.concat(
            [ergebnis_sortiert, close_series_today],
            axis=1,
            keys=["Momentum", "Close"],
        )

        concatiniert_ergebnis = concatiniert_ergebnis.sort_values(
            by="Momentum", ascending=False
        )

        momentum_geld = []
        momentum_close = []
        momentum_geld.extend([0] * self.parameter.anzahlAktien)
        momentum_close.extend([1] * self.parameter.anzahlAktien)

        ticker_namen = [f"Geld_{i+1}" for i in range(self.parameter.anzahlAktien)]
        new_tuples = [("Close", ticker) for ticker in ticker_namen]
        new_index = pd.MultiIndex.from_tuples(new_tuples, names=["Price", "Ticker"])

        new_row = pd.DataFrame(
            {"Momentum": momentum_geld, "Close": momentum_close}, index=new_index
        )

        # Anhängen
        # concatiniert_ergebnis = pd.concat([concatiniert_ergebnis, new_row])

        concatiniert_ergebnis.name = "Momentum: " + list(df.index)[pos].strftime(
            "%Y-%m-%d"
        )

        concatiniert_ergebnis = concatiniert_ergebnis.sort_values(
            by="Momentum", ascending=False
        )

        return concatiniert_ergebnis

    def sort_df(self, df):
        return df.sort_values(by="Momentum", ascending=False).copy()
