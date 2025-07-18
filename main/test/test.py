from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf

tickers = "DHL.DE"
start_date = "2020-01-17"
end_date = "2025-01-30"
data = yf.download(tickers, start=start_date, end=end_date)


print(data)
print(data[data.isna().any(axis=1)])
