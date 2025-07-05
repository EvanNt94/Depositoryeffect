import pandas as pd
import psycopg2

def load_price_data(isin: str, start: str, end: str) -> pd.DataFrame:
    conn = psycopg2.connect(
        host="localhost",
        database="tradx__price",
        user="a2"
    )
    cursor = conn.cursor()
    query = """
        SELECT timestamp, close
        FROM tradx_price
        WHERE isin = %s AND timestamp BETWEEN %s AND %s
        ORDER BY timestamp ASC;
    """
    cursor.execute(query, (isin, start, end))
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["date", "close"])
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    cursor.close()
    conn.close()
    return df