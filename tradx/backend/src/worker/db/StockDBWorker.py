from tradx.backend.src.worker.db.sql_templates import get_sql_template
from tradx.backend.src.worker.db.queue import write_queue
from tradx.backend.src.util.db.pg import get_async_pool

async def insert_stock(payload: dict):
    sql = get_sql_template("asset", "insert_stock")
    await write_queue.put({"sql": sql, "params": payload})

async def get_all_isins() -> list[str]:
    sql = get_sql_template("asset", "get_all_isins")
    async with (await get_async_pool()).acquire() as conn:
            rows = await conn.fetch(sql)
            return [row[0] for row in rows]

async def get_all_tickers() -> list[str]:
    sql = get_sql_template("asset", "get_all_tickers")
    async with (await get_async_pool()).acquire() as conn:
        rows = await conn.fetch(sql)
        return [row[0] for row in rows]

async def get_currency_by_isin(isin: str) -> str | None:
    sql = get_sql_template("asset", "get_currency_by_isin")
    async with (await get_async_pool()).acquire() as conn:
        row = await conn.fetchrow(sql, isin)
        return row[0] if row else None

async def get_ticker_by_isin(isin: str) -> str | None:
    sql = get_sql_template("asset", "get_ticker_by_isin")
    async with (await get_async_pool()).acquire() as conn:
        row = await conn.fetchrow(sql, isin)
        return row[0] if row else None

async def get_stock_by_isin(isin: str) -> dict | None:
    sql = get_sql_template("asset", "get_stock_by_isin")
    async with (await get_async_pool()).acquire() as conn:
        row = await conn.fetchrow(sql, isin)
        return dict(row) if row else None

async def get_column_by_isin(isin: str, column: str) -> str | int | float | None:
    sql = f"SELECT {column} FROM asset.stock WHERE isin = $1"
    async with (await get_async_pool()).acquire() as conn:
        row = await conn.fetchrow(sql, isin)
        return row[0] if row else None
    
async def is_defaulted(isin: str) -> bool:
    sql = "SELECT defaulted_timestamp FROM asset.stock WHERE isin = $1"
    async with (await get_async_pool()).acquire() as conn:
        val = await conn.fetchval(sql, isin)
        return val is not None and val != -1