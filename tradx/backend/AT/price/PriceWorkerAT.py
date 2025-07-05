from multiprocessing import Queue
from tradx.backend.src.worker.db.PriceDBHandler import PriceDBWorker as PDB
import pandas as pd
import requests as req
from io import BytesIO
from datetime import datetime

main_url = f"https://www.athexgroup.gr/en/market-data/statistics/eod-closing-prices/regulated/stocks/0/{datetime.now().strftime("%Y%m%d")}/xlsx"

def main(price_db:PDB):
    resp = req.get(main_url)
    xls = BytesIO(resp.content) 
    try:
        df = pd.read_excel(xls, engine="openpyxl")
    except:
        pass
    isins = []
    for idx, row in df.iterrows():
        isins.append(row["ISIN"])
        price_db.queue.put({
            "isin": row["ISIN"],
            "date": datetime.today(),
            "open": float(row["Opening"]) if not pd.isna(row["Opening"]) else None,
            "high": float(row["Max"]) if not pd.isna(row["Max"]) else None,
            "low": float(row["Min"]) if not pd.isna(row["Min"]) else None,
            "close": float(row["Price"]) if not pd.isna(row["Price"]) else None,
            "volume": int(row["Volume"]) if not pd.isna(row["Volume"]) else None,
            "trades": None,
        })
    return isins




if __name__ == "__main__":
    q = Queue()
    db = PDB(q)
    main(db)