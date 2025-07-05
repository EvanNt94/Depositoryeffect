import asyncpg
from tradx.backend.src.util.db.pg import get_async_pool
from tradx.backend.src.worker.db.sql_templates import get_sql_template
from typing import List

def map_underlying_params(p: dict) -> tuple:
    """
    Mapped underlying dict to positional SQL parameter tuple.
    """
    return (
        p["ticker"],
        p["isin"],
        p["has_option"],
    )

def map_option_params(p: dict) -> tuple:
    """
    Mapped option dict to positional SQL parameter tuple.
    """
    return (
        p["underlying_id"],
        p["type"],
        p["strike"],
        p["expiry"],
        p["option_symbol"],
    )

def map_option_greeks_params(p: dict) -> tuple:
    """
    Mapped option greeks dict to positional SQL parameter tuple.
    """
    return (
        p["option_id"], p["timestamp"],
        p["delta"], p["gamma"], p["vega"], p["theta"], p["rho"],
        p["iv"], p["price"],
        p["vomma"], p["charm"], p["vanna"], p["speed"], p["zomma"], p["color"], p["ultima"], p["veta"],
        p["source"], p["model_name"],
    )

def map_option_price_params(p: dict) -> tuple:
    """
    Mapped option price dict to positional SQL parameter tuple.
    """
    return (
        p["option_id"], p["timestamp"],
        p["spot_price"], p["bid"], p["bid_size"],
        p["ask"], p["ask_size"], p["last"], p["volume"], p["oi"], p["source"], p["incomplete"],
    )

async def get_option_id_by_symbol(symbol: str):
    """
    Retrieve option ID by option symbol.

    Returns the option's internal ID or None if not found.
    """
    sql = get_sql_template("option_reader", "get_option_id_by_symbol")
    async with (await get_async_pool()).acquire() as conn:
        row = await conn.fetchrow(sql, symbol)
        return row["id"] if row else None
    
async def get_all_underlyings_with_options() -> list[dict]:
    """
    Returns all underlyings that are marked as having options (has_option = true).
    Each result includes the internal ID and the ISIN.
    """
    sql = get_sql_template("option_reader", "get_all_underlyings_with_options")
    async with (await get_async_pool()).acquire() as conn:
        rows = await conn.fetch(sql)
        return [dict(row) for row in rows]
    
    
async def get_option_id(underlying_id: int, type_: str, strike: float, expiry):
    """
    Retrieve option ID by underlying ID, type, strike, and expiry.

    Returns the option's internal ID or None if not found.
    """
    sql = get_sql_template("option_reader", "get_option_id_full")
    async with (await get_async_pool()).acquire() as conn:
        row = await conn.fetchrow(sql, underlying_id, type_, strike, expiry)
        return row["id"] if row else None
    
async def get_underlying_id_by_isin(isin: str) -> int | None:
    """
    Returns the internal ID of an underlying by its ISIN, or None if not found.
    """
    sql = get_sql_template("option_reader", "get_underlying_id_by_isin")
    async with (await get_async_pool()).acquire() as conn:
        row = await conn.fetchrow(sql, isin)
        return row["id"] if row else None

async def get_underlying_by_isin(isin: str) -> dict | None:
    """
    Retrieve underlying data by ISIN.

    Returns a dictionary of underlying fields or None if not found.
    """
    sql = get_sql_template("option_reader", "get_underlying_by_isin")
    async with (await get_async_pool()).acquire() as conn:
        row = await conn.fetchrow(sql, isin)
        return dict(row) if row else None

async def insert_underlying(payload: dict) -> None:
    """
    Insert new underlying into database using asyncpg-compatible parameters.
    """
    sql = get_sql_template("option", "insert_underlying")
    async with (await get_async_pool()).acquire() as conn:
        await conn.execute(sql, *map_underlying_params(payload))
        

async def get_all_underlyings() -> list["asyncpg.Record"]:
    """
    Retrieve all underlying entries from the database.

    Returns a list of records or None if no entries exist.
    """
    sql = get_sql_template("option_reader", "get_all_underlyings")
    async with (await get_async_pool()).acquire() as conn:
        rows = await conn.fetch(sql)
        return rows



async def insert_option(payload: dict) -> None:
    """
    Insert new option into database using asyncpg-compatible parameters.
    """
    sql = get_sql_template("option", "insert_option")
    async with (await get_async_pool()).acquire() as conn:
        await conn.execute(sql, *map_option_params(payload))

async def insert_option_greeks(payload: dict) -> None:
    """
    Insert option greeks data into database using asyncpg-compatible parameters.
    """
    sql = get_sql_template("option", "insert_option_greeks")
    async with (await get_async_pool()).acquire() as conn:
        await conn.execute(sql, *map_option_greeks_params(payload))

async def insert_option_price(payload: dict) -> None:
    """
    Enqueue option price data for asynchronous insertion into the database.
    """
    sql = get_sql_template("option", "insert_option_price")
    from tradx.backend.src.worker.db.queue import write_queue
    await write_queue.put({"sql": sql, "params": map_option_price_params(payload)})

async def insert_option_prices_batch(payloads: List[dict]) -> None:
    """
    Enqueue batch of option price data for asynchronous insertion into the database.
    """
    if not payloads:
        return
    sql = get_sql_template("option", "insert_option_price")
    from tradx.backend.src.worker.db.queue import write_queue
    params = [map_option_price_params(p) for p in payloads]
    await write_queue.put({"sql": sql, "params": params})
async def get_active_isin_wo_underlying() -> list[str]:
    """
    Returns a list of ISINs from asset.stock that are active 
    (i.e. defaulted_timestamp = -1) and have no associated entry 
    in option.underlyings.

    Used to determine which assets still require option tracking setup.
    """
    sql = get_sql_template("option_reader", "get_active_isin_wo_underlying")
    async with (await get_async_pool()).acquire() as conn:
        rows = await conn.fetch(sql)
        return [r["isin"] for r in rows]
async def get_all_active_options() -> list[dict]:
    """
    Retrieve all options with expiry in the future, joined with ISINs from underlyings.

    Returns a list of dictionaries containing:
    - id
    - option_symbol
    - type
    - expiry
    - strike
    - isin
    """
    sql = get_sql_template("option_reader", "get_all_active_options")
    async with (await get_async_pool()).acquire() as conn:
        rows = await conn.fetch(sql)
        return [dict(row) for row in rows]