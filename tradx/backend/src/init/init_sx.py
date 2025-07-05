from pathlib import Path
import sqlite3


EXCHANGE_DB_PATH = Path.home() / "db" / "tradx" / "exchanges.db"

class StockExchangeDB:
    def __init__(self):
        self.conn = sqlite3.connect(EXCHANGE_DB_PATH)
        self.cursor = self.conn.cursor()

    def create_exchange_table(self, exchange_name: str):
        table_name = f"{exchange_name.lower()}_tickers"
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                ticker TEXT PRIMARY KEY,
                name TEXT,
                country TEXT,
                currency TEXT,
                last_updated TEXT
            )
        """)
        self.conn.commit()
