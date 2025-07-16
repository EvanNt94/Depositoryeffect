import csv
from datetime import datetime
from typing import List

import pandas as pd
import yfinance as yf


def fetch_and_save_yfinance_data(
    ticker_list: List[str], start_date: str, end_date: str
):
    all_dates = pd.date_range(start=start_date, end=end_date, freq="B")
    all_dates_str = [d.strftime("%Y-%m-%d") for d in all_dates]

    header = ["Ticker", "ISIN"]
    for date in all_dates_str:
        header.extend([date, f"{date}_open", f"{date}_close"])

    for ticker in ticker_list:
        print(f"Fetching {ticker}...")
        error_msg = ""
        isin = ""
        hist = pd.DataFrame()
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date)
            isin = stock.info.get("isin", "")
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            error_msg = str(e)
        finally:
            output_csv = f"{ticker}_{start_date}_{end_date}.csv"
            if not hist.empty:
                hist_dates = pd.to_datetime(hist.index).strftime("%Y-%m-%d")
                hist_dates_list = list(hist_dates)
                row = [ticker, isin]
                for date in all_dates_str:
                    if date in hist_dates_list:
                        idx = hist_dates_list.index(date)
                        open_price = hist.iloc[idx]["Open"]
                        close_price = hist.iloc[idx]["Close"]
                    else:
                        open_price = ""
                        close_price = ""
                    row.extend([date, open_price, close_price])
                try:
                    with open(output_csv, "w", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow(header)
                        writer.writerow(row)
                    print(f"Datei geschrieben: {output_csv}")
                except Exception as file_err:
                    print(f"Fehler beim Schreiben der Datei {output_csv}: {file_err}")
            else:
                try:
                    with open(output_csv, "w", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow(["Ticker", "ISIN", "Error"])
                        writer.writerow([ticker, isin, error_msg])
                    print(f"Datei geschrieben: {output_csv}")
                except Exception as file_err:
                    print(f"Fehler beim Schreiben der Datei {output_csv}: {file_err}")


if __name__ == "__main__":
    fetch_and_save_yfinance_data(["AAPL", "TSLA"], "2000-01-01", "2021-12-31")
