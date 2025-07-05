from tradx.backend.src.worker.db.queue import write_queue
from tradx.backend.src.worker.db.sql_templates import get_sql_template
from typing import Dict, Any, List

async def insert_fundamentals(payload: Dict[str, Any]) -> None:
    sql = get_sql_template("fundamentals", "insert_fundamentals")
    await write_queue.put({
        "sql": sql,
        "params": payload
    })

async def insert_fundamentals_batch(payloads: List[Dict[str, Any]]) -> None:
    if not payloads:
        return
    sql = get_sql_template("fundamentals", "insert_fundamentals")
    await write_queue.put({
        "sql": sql,
        "params": payloads
    })
