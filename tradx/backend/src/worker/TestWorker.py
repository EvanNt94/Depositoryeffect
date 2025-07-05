import json
import time
from backend.src.worker.db.StockDBWorker import StockDBWorker
import yfinance as yf
from multiprocessing import Queue 

class StockDBHelper:
    def __init__(self, db_path):
        self.db_path = db_path

    def recently_updated(self, isin: str) -> bool:
        import sqlite3, time
        threshold = int(time.time()) - 90 * 86400
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT last_updated FROM stock WHERE isin = ?", (isin,))
            row = cur.fetchone()
            return row is not None and row[0] is not None and row[0] >= threshold

class TestWorker:
    def __init__(self, queue:Queue):
        self.queue = queue

    def run(self, isin:str, debug=False):
        try:
            ticker = yf.Ticker(isin)
        except ValueError:
            print(isin+ " not on yfinance.")
            prior:list = json.loads(open("/Users/a2/code/fin/trade/tradx/data/ticker/not_in_yfinance.json").read())
            prior.append(isin)
            open("/Users/a2/code/fin/trade/tradx/data/ticker/not_in_yfinance.json", "w").write(json.dumps(prior))
            return
        try:
            info = ticker.info
        except:
            print("error with isin "+ isin)
            prior:list = json.loads(open("/Users/a2/code/fin/trade/tradx/data/ticker/not_in_yfinance.json").read())
            prior.append(isin)
            open("/Users/a2/code/fin/trade/tradx/data/ticker/not_in_yfinance.json", "w").write(json.dumps(prior))
            return
        if debug: print(info)
        dd = {}
        dd["ticker"] = info.get("symbol")
        dd["isin"] = isin
        dd["name"] = info.get("displayName", info.get("longName"))
        dd["longName"] = info.get("longName")
        dd["website"] = info.get("website")
        dd["industryKey"] = info.get("industryKey")
        dd["sectorKey"] = info.get("sectorKey")
        dd["summary"] = info.get("longBusinessSummary")
        dd["employees"] = info.get("fullTimeEmployees", None)
        dd["irWebsite"] = info.get("irWebsite", None)
        dr = info.get("dividendRate", None)
        pc = info.get("previousClose", 0)
        if pc == 0:
            dd["dividend"] = None
        else:
            dd["dividend"] = dr / pc if dr is not None else None

        dd["fiveYearAvgDividendYield"] = info.get("fiveYearAvgDividendYield", None)
        dd["beta"] = info.get("beta")
        dd["street"] = info.get("address1")
        dd["city"] = info.get("city")
        dd["zip"] = info.get("zip")
        dd["state"] = info.get("state", None)
        dd["country"] = info.get("country")
        dd["currency"] = info.get("currency")
        dd["region"] = info.get("region")
        dd["ipo"] = info.get("firstTradeDateMilliseconds")
        dd["last_updated"] = int(time.time())
        self.queue.put({"type": "insert_stock", "payload": dd})



if __name__ == "__main__":
    not_yf = json.loads(open("/Users/a2/code/fin/trade/tradx/data/ticker/not_in_yfinance.json").read())
    isins = json.loads(open("/Users/a2/code/fin/trade/tradx/backend/traderepublic/instruments.json").read()).keys()
    queue = Queue()
    db_worker = StockDBWorker(queue)
    db_worker.start()
    helper = StockDBHelper("/Users/a2/db/tradx/stock.db")
    worker = TestWorker(queue)
    for isin in isins:
        if helper.recently_updated(isin):
            continue
        if isin in not_yf:
            continue
        worker.run(isin)
        time.sleep(0.5)
    queue.put(None)
    db_worker.join()
