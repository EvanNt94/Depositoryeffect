from asyncio import Queue
import logging
import os
from tradx.backend.src.util.db.pg import get_async_pool
from tradx.backend.src.worker.db.queue import write_queue

async def run_db_worker():
    print("[DBWorker] started")
    debug = os.getenv("DEBUG", False)
    """
    Worker, der DB-Schreibaufgaben aus der Queue verarbeitet.
    Erkennt, ob eine Aufgabe ein einzelner Datensatz (dict) oder ein Batch (list) ist.
    """
    while True:
        task = await write_queue.get()
        sql = task["sql"]
        params = task["params"]

        try:
            # Holen der Verbindung für die Aufgabe/den Batch
            async with (await get_async_pool()).acquire() as conn:
                    # Prüfen, ob `params` eine Liste ist -> Batch-Operation
                    if isinstance(params, list):
                        if not params: # Leeren Batch ignorieren
                            continue 
                        if debug: print(f"[DBWorker] Executing BATCH of {len(params)} items.")
                        # executemany ist für Batches optimiert
                        await conn.executemany(sql, params)
                    else:
                        # `params` ist ein dict -> Einzelne Operation
                        if debug: print(f"[DBWorker] Executing SINGLE item.")
                        await conn.execute(sql, *params)
        except Exception as e:
            # Bei Fehlern nur die ersten paar Parameter loggen, um das Log nicht zu fluten
            log_params = params[0] if isinstance(params, list) and params else params
            logging.error(f"DB Worker error executing SQL: {sql}, params (sample): {log_params}, error: {e}")
        finally:
            write_queue.task_done()