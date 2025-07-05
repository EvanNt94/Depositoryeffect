from pathlib import Path
from tradx.backend.src.util.db.pg import get_async_pool
from tradx.backend.src.worker.db.sql_templates import get_sql_template  
from tradx.backend.src.worker.db.queue import write_queue

async def insert_or_update_ticker(payload: dict):
    sql = get_sql_template("exchange", "insert_or_update_ticker")
    await write_queue.put({"sql": sql, "params": payload})

async def get_isin_from_ticker(ticker: str) -> list[str]:
    sql = get_sql_template("exchange", "get_isin_from_ticker")
    async with get_async_pool().acquire() as conn:
        rows = await conn.fetch(sql, {"ticker": ticker})
        return [row["isin"] for row in rows]

async def get_ticker_from_local(exchange: str, ticker_local: str) -> list[str]:
    sql = get_sql_template("exchange", "get_ticker_from_local")
    async with get_async_pool().acquire() as conn:
        rows = await conn.fetch(sql, {"exchange": exchange, "ticker_local": ticker_local})
        return [row["ticker"] for row in rows]