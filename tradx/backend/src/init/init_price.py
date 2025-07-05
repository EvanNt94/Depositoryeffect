import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="tradx__price",
    user="a2"
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS tradx_price (
    isin          TEXT NOT NULL,
    timestamp     TIMESTAMPTZ NOT NULL,
    open          DOUBLE PRECISION,
    high          DOUBLE PRECISION,
    low           DOUBLE PRECISION,
    close         DOUBLE PRECISION,
    volume        BIGINT,
    last_updated  TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (isin, timestamp)
);
""")

cur.execute("""
CREATE INDEX IF NOT EXISTS idx_tradx_price_isin ON tradx_price (isin);
""")

cur.execute("""
CREATE INDEX IF NOT EXISTS idx_tradx_price_ts ON tradx_price (timestamp DESC);
""")

conn.commit()
cur.close()
conn.close()