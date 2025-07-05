from pathlib import Path
import sqlite3
from filelock import FileLock
from datetime import datetime, timedelta
from  tradx.backend.src.risk.risk_free_rate import get_risk_free_rate

DB_PATH = Path.home() / "db" / "tradx" / "rate.db"
LOCKFILE = Path.home() / "db" / "tradx" / "rate.lock"

# Create the risk_free_rates table if it does not exist
def create_table():
    with FileLock(LOCKFILE):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS risk_free_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency TEXT NOT NULL,
                rate REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

def get_latest_risk_free_rate(currency: str = "USD") -> float:
    create_table()
    with FileLock(LOCKFILE):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT rate, timestamp FROM risk_free_rates
            WHERE currency = ?
            ORDER BY timestamp DESC
            LIMIT 1
        """, (currency,))
        row = cursor.fetchone()

        if row:
            rate, timestamp_str = row
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
            except:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            if datetime.now() - timestamp < timedelta(hours=24):
                conn.close()
                return rate

        rate = get_risk_free_rate(currency)
        cursor.execute("""
            INSERT INTO risk_free_rates (currency, rate, timestamp)
            VALUES (?, ?, ?)
        """, (currency, rate, datetime.now()))
        conn.commit()
        conn.close()
        return rate

def insert_risk_free_rate(currency: str, rate: float):
    with FileLock(LOCKFILE):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO risk_free_rates (currency, rate, timestamp)
            VALUES (?, ?, ?)
        """, (currency, rate, datetime.now()))
        conn.commit()
        conn.close()