from datetime import datetime, timedelta

import pandas as pd
from strategies.strategy import Strategy


class RSIStrategy(Strategy):

    def __init__(self):
        super().__init__()
        self.momentum_days = 30
        self.strategy_name = "RSI Period"
        self.rsi_period = 14

    def sort_stocks(self, actual_pos, df):
        # (Preis heute / Preis vor 30 Tagen) -1
        # Sortieren

        # start_date = start_date_ts.strftime("%Y-%m-%d")
        # print("Sort Stocks Momentum", start_date)

        # print(list(map(lambda i: i.strftime("%Y-%m-%d"), list(df.index))))

        # pos = df.index.get_loc(start_date)
        pos = actual_pos
        close_series_today = df.iloc[pos]
        df_letzte_15 = df.iloc[(pos - self.rsi_period - 10) : pos]

        # Concatenaten
        concatiniert_ergebnis = pd.concat(
            [close_series_today],
            axis=1,
            keys=["Close"],
        )

        rsi_data = {}

        for ticker in df_letzte_15["Close"].columns:
            close_series = df_letzte_15["Close"][ticker]
            rsi_series = self.berechne_rsi(close_series, window=self.rsi_period)
            rsi_data[ticker] = rsi_series

        rsi_df = pd.Series(rsi_data, name="RSI")
        rsi_df.index = pd.MultiIndex.from_product([["Close"], rsi_df.index])
        concatiniert_ergebnis["RSI"] = rsi_df
        concatiniert_ergebnis = concatiniert_ergebnis.sort_values(
            by="RSI", ascending=True
        )

        concatiniert_ergebnis.name = "RSI: " + list(df.index)[pos].strftime("%Y-%m-%d")

        return concatiniert_ergebnis

    def berechne_rsi(self, close_prices: pd.Series, window: int = 14) -> pd.Series:
        delta = close_prices.diff()

        # Gewinne und Verluste trennen
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # Gleitender Durchschnitt (Exponentiell oder Simple)
        avg_gain = gain.rolling(window=window, min_periods=window).mean()
        avg_loss = loss.rolling(window=window, min_periods=window).mean()

        # Relative Strength (RS)
        rs = avg_gain / avg_loss

        # RSI berechnen
        rsi = 100 - (100 / (1 + rs.iloc[-1]))
        return rsi

    def sort_df(self, df):
        return df.sort_values(by="RSI", ascending=True).copy()
