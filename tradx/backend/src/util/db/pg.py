import asyncpg
from os import environ

_async_pool: asyncpg.Pool | None = None

def _build_conninfo() -> str:
    return (
        f"postgresql://{environ.get('PGUSER', 'a2')}@{environ.get('PGHOST', 'localhost')}/"
        f"{environ.get('PGDATABASE', 'tradx')}"
    )

async def get_async_pool() -> asyncpg.Pool:
    global _async_pool
    if _async_pool is None:
        _async_pool = await asyncpg.create_pool(
            dsn=_build_conninfo(),
            min_size=1,
            max_size=16,
        )
    return _async_pool