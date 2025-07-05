from tradx.backend.src.util.db.pg import get_async_pool
from tradx.backend.src.worker.db.sql_templates import get_sql_template
from typing import List



def map_rss_params(p: dict) -> tuple:
    """
    Mapped underlying dict to positional SQL parameter tuple.
    """
    return (
        p["url"],
        p["type"],
        p["exchange"],
        p["lang"],
    )
    

# New function to retrieve all RSS sources with extended metadata
from typing import List

async def get_rss_sources_full() -> List[dict]:
    """
    Retrieve all RSS sources with extended metadata.
    """
    sql = "SELECT url, type, exchange, lang FROM sources.rss;"
    async with (await get_async_pool()).acquire() as conn:
        rows = await conn.fetch(sql)
        return [dict(row) for row in rows]

async def get_rss_sources(symbol: str):
    """
    Retrieve option ID by option symbol.

    Returns the option's internal ID or None if not found.
    """
    sql = "SELECT r.url FROM sources.rss ;"
    async with (await get_async_pool()).acquire() as conn:
        row = await conn.fetchrow(sql, symbol)
        return row["id"] if row else None
    



async def insert_rss_entries(pool, entries):
    insert_rss_sql = get_sql_template("rss", "insert_rss_entry")
    
    async with (await get_async_pool()).acquire() as conn:
            for entry in entries:
                await conn.execute(
                    insert_rss_sql,
                    entry["id"],
                    entry["feed"],
                    entry["title"],
                    entry["link"],
                    entry["summary"],
                    entry["date"],
                    entry["company"],
                    entry["ticker"],
                    entry["isin"],
                    entry["language"],
                    entry["attachment_url"],
                    entry["pdf_path"],
                    entry["last_updated"],
                )
