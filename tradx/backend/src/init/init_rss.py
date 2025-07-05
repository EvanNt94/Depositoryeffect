from pathlib import Path
import sqlite3
import os

DB_DIR = Path.home() / "db" / "tradx"
DB_DIR.mkdir(parents=True, exist_ok=True)

# stock.db for stock table
DB_PATH = DB_DIR / "rss_signals.db"

def init_rss_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS rss_entry (
            id TEXT PRIMARY KEY,
            feed TEXT,
            title TEXT,
            link TEXT,
            summary TEXT,
            date TEXT,
            company TEXT,
            ticker TEXT,
            isin TEXT,
            language TEXT,
            attachment_url TEXT,
            pdf_path TEXT,
            last_updated TEXT
        );
    """)
    conn.commit()
    conn.close()
    print("Initialized rss_signals.db at", DB_PATH)


if __name__ == "__main__":
    init_rss_db()