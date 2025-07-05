from tradx.backend.src.worker.db.sql_templates import get_sql_template
from tradx.backend.src.util.db.pg import get_async_pool

async def insert_rss_entry(payload: dict) -> None:
    sql = get_sql_template("rss", "insert_rss_entry")
    async with get_async_pool().acquire() as conn:
        await conn.execute(sql, payload)