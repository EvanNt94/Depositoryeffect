from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from strategies.strategy import Strategy


class MovingAverageCrossoverStrategy(Strategy):

    def __init__(self):
        super().__init__()
        self.momentum_days = 30
        self.strategy_name = "Moving Average Crossover"

    def sort_stocks(self, actual_pos, df):
        # (Preis heute / Preis vor 30 Tagen) -1
        # Sortieren

        # start_date = start_date_ts.strftime("%Y-%m-%d")
        # print("Sort Stocks Momentum", start_date)

        # print(list(map(lambda i: i.strftime("%Y-%m-%d"), list(df.index))))

        # pos = df.index.get_loc(start_date)
        pos = actual_pos
        close_series_today = df.iloc[pos]
        df_letzte_200 = df.iloc[(pos - 203) : pos]

        # Concatenaten
        concatiniert_ergebnis = pd.concat(
            [close_series_today],
            axis=1,
            keys=["Close"],
        )

        sma_50 = df_letzte_200.rolling(window=50).mean()
        sma_200 = df_letzte_200.rolling(window=200).mean()
        sma_50_shifted = sma_50.shift(1)
        sma_200_shifted = sma_200.shift(1)

        # Letzte Zeile als Series mit allen Tickern
        sma_50_last = sma_50.iloc[-1]
        sma_200_last = sma_200.iloc[-1]
        sma_50_shifted_last = sma_50_shifted.iloc[-1]
        sma_200_shifted_last = sma_200_shifted.iloc[-1]
        signal = np.where(
            (sma_50_shifted_last < sma_200_shifted_last)
            & (sma_50_last >= sma_200_last),
            sma_50_last
            - sma_200_last,  # Differenz nur für die letzte Zeile und alle Ticker
            0,
        )
        columns = df_letzte_200.columns
        tickers = [t[1] for t in columns]

        signal_series = pd.Series(signal, index=tickers)
        signal_series.index = pd.MultiIndex.from_product(
            [["Close"], signal_series.index]
        )

        concatiniert_ergebnis["Signal"] = signal_series

        concatiniert_ergebnis = concatiniert_ergebnis.sort_values(
            by="Signal", ascending=False
        )

        concatiniert_ergebnis.name = "Signal: " + list(df.index)[pos].strftime(
            "%Y-%m-%d"
        )

        return concatiniert_ergebnis

    def sort_df(self, df):
        return df.sort_values(by="Signal", ascending=False).copy()
