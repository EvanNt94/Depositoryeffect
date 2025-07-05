import pandas as pd
from strategies.strategy import Strategy
from datetime import datetime, timedelta


class MomentumStrategy(Strategy):

    def __init__(self):
        super().__init__()
        self.momentum_days = 180

    def generate_signals(self) -> pd.DataFrame:
        df = self.data.copy()
        df["Signal"] = 0
        holding = False
        buy_price = 0

        for i in range(1, len(df)):
            price = df["Close"].iloc[i]

            if not holding:
                df.iloc[i, df.columns.get_loc("Signal")] = 1  # Buy
                holding = True
                buy_price = price
            else:
                change = (price - buy_price) / buy_price
                if change > 0.05:
                    df.iloc[i, df.columns.get_loc("Signal")] = -1  # Sell
                    holding = False
                    buy_price = 0
                else:
                    df.iloc[i, df.columns.get_loc("Signal")] = 0  # Hold

        return df

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

        concatiniert_ergebnis.name = "Momentum: " + list(df.index)[pos].strftime(
            "%Y-%m-%d"
        )

        return concatiniert_ergebnis

    def sort_df(self, df):
        return df.sort_values(by="Momentum", ascending=False).copy()
