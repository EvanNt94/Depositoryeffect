from tradx.backend.src.options.option_schema import underlyings_schema
import datetime

def set_defaulted(isin: str, timestamp: int):
    from tradx.backend.src.worker.db.StockDBWorker import DB_PATH, LOCKFILE
    import sqlite3
    import fcntl

    class WriteLock:
        def __init__(self, path):
            self.path = path
            self.handle = None

        def __enter__(self):
            self.handle = open(self.path, "w")
            fcntl.flock(self.handle, fcntl.LOCK_EX)

        def __exit__(self, *args):
            fcntl.flock(self.handle, fcntl.LOCK_UN)
            self.handle.close()

    with WriteLock(LOCKFILE):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE stock SET defaulted_timestamp = ? WHERE isin = ?",
            (timestamp, isin)
        )
        conn.commit()
        conn.close()



def set_all_defaulted_timestamp(ts: int):
    from tradx.backend.src.worker.db.StockDBWorker import DB_PATH, LOCKFILE
    import sqlite3
    import fcntl

    class WriteLock:
        def __init__(self, path):
            self.path = path
            self.handle = None

        def __enter__(self):
            self.handle = open(self.path, "w")
            fcntl.flock(self.handle, fcntl.LOCK_EX)

        def __exit__(self, *args):
            fcntl.flock(self.handle, fcntl.LOCK_UN)
            self.handle.close()

    with WriteLock(LOCKFILE):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE stock SET defaulted_timestamp = ?", (ts,))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    # set_all_defaulted_timestamp(-1)
    # exit(0)
    # Beispiel: AU000000CDD7 delisted am 17. Jan 2025
    dt = datetime.datetime(2024, 12, 18)
    ts = int(dt.timestamp())
    set_defaulted("AU000000CE10", ts)