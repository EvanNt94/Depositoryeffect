import logging

from config.config import BASKETS
from frontend.main import MainFrame
from stockexchange.fetch_stock.YFinanceFetcher import YFinanceFetcher
from stockexchange.FetchStock import FetchStock


def __main__():
    pass


# tickers = BASKETS["Nasdaq 100 Tech-Stocks"]
# start_date = "2025-01-01"
# ‚end_date = "2025-05-12"

# stockexchange = FetchStock(tickers, start_date, end_date, YFinanceFetcher())
# data = stockexchange.fetch_data()
# print(data)

main_frame = MainFrame()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] [%(module)s.%(funcName)s] [%(lineno)d] %(message)s",
)
