import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def init_db():
    conn = psycopg2.connect(
        dbname="tradx__opt",
        user="a2",
        host="localhost",
        port="5432"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Tabelle für Underlyings
    cur.execute("""
    CREATE TABLE IF NOT EXISTS underlyings (
        id SERIAL PRIMARY KEY,
        ticker TEXT NOT NULL,
        isin TEXT,
        name TEXT,
        has_option BOOLEAN DEFAULT FALSE
    );
    """)

    # Tabelle für Optionen
    cur.execute("""
    CREATE TABLE IF NOT EXISTS options (
        id SERIAL PRIMARY KEY,
        underlying_id INTEGER NOT NULL REFERENCES underlyings(id),
        type TEXT CHECK(type IN ('CALL', 'PUT')) NOT NULL,
        strike DOUBLE PRECISION NOT NULL,
        expiry DATE NOT NULL,
        option_symbol TEXT UNIQUE NOT NULL
    );
    """)

    # Tabelle für Optionspreise
    cur.execute("""
    CREATE TABLE IF NOT EXISTS option_prices (
        id SERIAL PRIMARY KEY,
        option_id INTEGER NOT NULL REFERENCES options(id),
        timestamp TIMESTAMPTZ NOT NULL,
        spot_price DOUBLE PRECISION,
        bid DOUBLE PRECISION,
        bid_size INTEGER,
        ask DOUBLE PRECISION,
        ask_size INTEGER,
        last DOUBLE PRECISION,
        volume INTEGER,
        oi INTEGER,
        iv DOUBLE PRECISION,
        delta DOUBLE PRECISION,
        gamma DOUBLE PRECISION,
        theta DOUBLE PRECISION,
        vega DOUBLE PRECISION,
        rho DOUBLE PRECISION,
        source TEXT,
        model_price DOUBLE PRECISION,
        iv_bid DOUBLE PRECISION,
        iv_ask DOUBLE PRECISION,
        incomplete BOOLEAN,
        anomaly_score DOUBLE PRECISION
    );
    """)

    # Indexe für Performance
    cur.execute("CREATE INDEX IF NOT EXISTS idx_options_underlying_id ON options (underlying_id);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_options_expiry ON options (expiry);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_option_prices_option_id_ts ON option_prices (option_id, timestamp DESC);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_option_prices_iv ON option_prices (iv);")

    cur.execute("""
    CREATE OR REPLACE VIEW v_options_active AS
    SELECT *
    FROM options
    WHERE expiry >= CURRENT_DATE;
    """)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    init_db()