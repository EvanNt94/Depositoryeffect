from datetime import timedelta, datetime
from stockexchange.fetch_stock.StockFetcher import StockFetcher
import yfinance as yf
import pandas as pd


class YFinanceFetcher(StockFetcher):
    def __init__(self):
        super().__init__()

    def fetch_stock(self, tickers, start_date, end_date):
        datum = datetime.strptime(start_date, "%Y-%m-%d")
        neues_datum = datum - timedelta(days=60)
        start_date_30d = neues_datum.strftime("%Y-%m-%d")

        data = yf.download(tickers, start=start_date_30d, end=end_date)
        return data

    def get_market_cap(self, series):
        print("In Markt Cap")
        tickers = list(series.columns.get_level_values(1))

        series_outstanding = pd.Series(
            index=tickers, dtype=float, name="Outstanding Shares"
        )
        series_outstanding.index.name = "Ticker"

        for ticker in tickers:

            yfTicker = yf.Ticker(ticker)
            shares_outstanding = yfTicker.info.get("sharesOutstanding", 0)

            series_outstanding[ticker] = shares_outstanding

        return series_outstanding
