from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf
from stockexchange.fetch_stock.StockFetcher import StockFetcher


class YFinanceFetcher(StockFetcher):
    def __init__(self):
        super().__init__()
        self.tickers = []
        self.gewinn = {}
        self.eps = {}

    def fetch_stock(self, tickers, start_date, end_date):
        self.tickers = tickers
        self.get_gewinn()
        datum = datetime.strptime(start_date, "%Y-%m-%d")
        neues_datum = datum - timedelta(days=400)
        start_date_30d = neues_datum.strftime("%Y-%m-%d")

        data = yf.download(tickers, start=start_date_30d, end=end_date)
        print(data)
        data = data.dropna(axis=1, how="all")
        print(data)
        # exit()
        return data

    def get_market_cap(self, series):
        print("In Markt Cap")
        tickers = list(series.columns.get_level_values(1))

        series_outstanding = pd.Series(
            index=tickers, dtype=float, name="Outstanding Shares"
        )
        series_outstanding.index.name = "Ticker"

        for ticker in tickers:
            try:

                yfTicker = yf.Ticker(ticker)
                # print(ticker)
                shares_outstanding = yfTicker.info.get("sharesOutstanding", 0)

                series_outstanding[ticker] = shares_outstanding
            except:
                series_outstanding[ticker] = 0

        return series_outstanding

    def get_gewinn(self):

        for ticker in self.tickers:
            yf_ticker = yf.Ticker(ticker)
            earnings = yf_ticker.income_stmt  # Jahreszahlen (Jahresabschluss)
            if "Net Income" in earnings.index:
                net_income_yearly = earnings.loc["Net Income"]
                net_income_dict = {
                    date.year: value
                    for date, value in net_income_yearly.items()
                    if pd.notna(value)
                }
                self.gewinn[ticker] = net_income_dict
            else:
                self.gewinn[ticker] = {}
                self.eps[ticker] = {}
                continue

            if "Diluted EPS" in earnings.index:
                net_income_yearly = earnings.loc["Diluted EPS"]
                net_income_dict = {
                    date.year: value
                    for date, value in net_income_yearly.items()
                    if pd.notna(value)
                }
                self.eps[ticker] = net_income_dict
