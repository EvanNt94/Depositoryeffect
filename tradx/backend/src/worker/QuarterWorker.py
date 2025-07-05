import time
from backend.src.worker.db.StockDBWorker import DBWorker

class QuarterWorker:
    def __init__(self, db_worker:DBWorker):
        self.db = db_worker

    