from multiprocessing import Queue
from tqdm import tqdm
import pandas as pd
import time
import asyncio
from tradx.backend.src.worker.db.PriceDBHandler import insert_price
from tradx.backend.src.worker.db.StockDBWorker import *
from tradx.backend.src.worker.db.TradxDBWorker import run_db_worker, write_queue
import yfinance as yf



async def process_price(isin: str):
    try:
        ticker = yf.Ticker(isin)
    except BaseException as e:
        print("isin: "+isin)
        print(e)
        return
        
    df = ticker.history(period="1d") # TODO 1d
    for idx, row in df.iterrows():
        payload = {
            "isin": isin,
            "date": idx.to_pydatetime(),
            "open": float(row["Open"]) if not pd.isna(row["Open"]) else None,
            "high": float(row["High"]) if not pd.isna(row["High"]) else None,
            "low": float(row["Low"]) if not pd.isna(row["Low"]) else None,
            "close": float(row["Close"]) if not pd.isna(row["Close"]) else None,
            "volume": int(row["Volume"]) if not pd.isna(row["Volume"]) else None,
            "trades": None,
        }
        await insert_price(payload)
    

async def main():
    worker_task = asyncio.create_task(run_db_worker())
    isins = await get_all_isins()
    print(len(isins))
    for isin in tqdm(isins):
        ## TODO hier nach SX routen
        await asyncio.sleep(1)
        await process_price(isin)
    await write_queue.join() 
    worker_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())