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

        # Concatenaten
        concatiniert_ergebnis = pd.concat(
            [close_series_today],
            axis=1,
            keys=["Close"],
        )

        concatiniert_ergebnis["RSI"] = (
            concatiniert_ergebnis["Close"].rolling(window=50).mean()
        )
        concatiniert_ergebnis["SMA_200"] = (
            concatiniert_ergebnis["Close"].rolling(window=200).mean()
        )

        # Crossover-Signale erzeugen
        concatiniert_ergebnis["Signal"] = 0
        # Buy
        mask = (
            concatiniert_ergebnis["SMA_50"].shift(1)
            < concatiniert_ergebnis["SMA_200"].shift(1)
        ) & (concatiniert_ergebnis["SMA_50"] >= concatiniert_ergebnis["SMA_200"])

        concatiniert_ergebnis.loc[mask, "Signal"] = (
            concatiniert_ergebnis.loc[mask, "SMA_50"]
            - concatiniert_ergebnis.loc[mask, "SMA_200"]
        )

        concatiniert_ergebnis["Outstanding Shares"] = self.outstanding_shares
        concatiniert_ergebnis["Market Cap"] = (
            concatiniert_ergebnis["Close"] * self.outstanding_shares
        )

        concatiniert_ergebnis = concatiniert_ergebnis.sort_values(
            by="Signal", ascending=False
        )

        concatiniert_ergebnis.name = "Signal: " + list(df.index)[pos].strftime(
            "%Y-%m-%d"
        )

        return concatiniert_ergebnis

    def berechne_rsi(close_prices: pd.Series, window: int = 14) -> pd.Series:
        delta = close_prices.diff()

        # Gewinne und Verluste trennen
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        # Gleitender Durchschnitt (Exponentiell oder Simple)
        avg_gain = gain.rolling(window=window, min_periods=window).mean()
        avg_loss = loss.rolling(window=window, min_periods=window).mean()

        # Relative Strength (RS)
        rs = avg_gain / avg_loss

        # RSI berechnen
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def sort_df(self, df):
        return df.sort_values(by="Signal", ascending=False).copy()
