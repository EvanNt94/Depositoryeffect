import yaml
from pathlib import Path
from typing import List, Dict, Any
from tradx.backend.src.worker.db.TradxDBWorker import write_queue

_sql_templates = None

def _load_sql_templates():
    global _sql_templates
    if _sql_templates is None:
        path = Path(__file__).resolve().parents[3] / "sql_templates" / "price.yaml"
        with open(path, "r") as f:
            _sql_templates = yaml.safe_load(f)
    return _sql_templates

def map_price_params(p: dict) -> tuple:
    return (
        p["isin"], p["date"], p["open"], p["high"],
        p["low"], p["close"], p["volume"]
    )

# Deine bestehende Funktion bleibt für Flexibilität erhalten
async def insert_price(payload: Dict[str, Any], debug=False):
    """Legt eine einzelne Preis-Einfüge-Aufgabe in die Queue."""
    if debug: print(f"[insert_price] Putting single price to write_queue: {payload.get('isin')} {payload.get('date')}")
    sql_templates = _load_sql_templates()
    sql = sql_templates["insert_price"]
    await write_queue.put({"sql": sql, "params": map_price_params(payload)})

# NEUE BATCH-FUNKTION
async def insert_prices_batch(payloads: List[Dict[str, Any]],debug=False):
    """Legt eine Batch-Preis-Einfüge-Aufgabe in die Queue."""
    if not payloads:
        return # Nichts zu tun

    if debug: print(f"[insert_prices_batch] Putting batch of {len(payloads)} prices to write_queue.")
    sql_templates = _load_sql_templates()
    sql = sql_templates["insert_price"] # Wir verwenden dasselbe SQL-Statement
    
    params = [map_price_params(p) for p in payloads]
    await write_queue.put({"sql": sql, "params": params})