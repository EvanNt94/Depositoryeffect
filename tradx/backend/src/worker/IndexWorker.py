from tqdm import tqdm
import pandas as pd
import time
from tradx.backend.src.worker.db.PriceDBHandler import PriceDBWorker as PDB
from tradx.backend.src.worker.db.StockDBWorker import StockDBWorker as StockDB
import yfinance as yf
from multiprocessing import Queue 

STOCK_DB = StockDB(Queue())
ISINS = STOCK_DB.get_isins()


def process_price(isin: str, price_db: PDB):
    try:
        ticker = yf.Ticker(isin)
    except BaseException as e:
        print("isin: "+isin)
        print(e)
        return
        
    df = ticker.history(period="max") # TODO 1d
    for idx, row in df.iterrows():
        price_db.queue.put({
            "isin": isin,
            "date": idx.to_pydatetime(),
            "open": float(row["Open"]) if not pd.isna(row["Open"]) else None,
            "high": float(row["High"]) if not pd.isna(row["High"]) else None,
            "low": float(row["Low"]) if not pd.isna(row["Low"]) else None,
            "close": float(row["Close"]) if not pd.isna(row["Close"]) else None,
            "volume": int(row["Volume"]) if not pd.isna(row["Volume"]) else None,
            "trades": None,
        })
    

def main():
    queue = Queue()
    price_db = PDB(queue)
    price_db.start()
    for isin in tqdm(ISINS):
        ## TODO hier nach SX routen
        time.sleep(1)
        process_price(isin, price_db)
    queue.put(None)
    price_db.join()

if __name__ == "__main__":
    main()