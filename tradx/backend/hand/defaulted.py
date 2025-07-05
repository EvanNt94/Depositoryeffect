from datetime import datetime
from multiprocessing import Queue
from tradx.backend.src.worker.db.StockDBWorker import StockDBWorker

import multiprocessing; multiprocessing.set_start_method("fork")

if __name__ == "__main__":
    q = Queue()
    sdb = StockDBWorker(q)
    sdb.start()
    dt = datetime.strptime("02 11, 2023", "%m %d, %Y")
    isin = "CA18453N1033"
    stock = sdb.get_info_by_isin(isin=isin)
    payload = dict(stock)
    payload["defaulted_timestamp"] = int(dt.timestamp())
    sdb.queue.put({"type": "update_defaulted", "payload": payload})
    sdb.queue.put(None)
    sdb.join()