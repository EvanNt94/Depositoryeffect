from queue import Empty
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class OptionTableSchema:
    name: str
    columns: List[str]
    primary_key: Optional[str] = None
    unique_key: Optional[str] = None

# Beispiele
underlyings_schema = OptionTableSchema(
    name="underlyings",
    columns=["id", "ticker", "isin", "name"],
    primary_key="id"
)

options_schema = OptionTableSchema(
    name="options",
    columns=["id", "underlying_id", "type", "strike", "expiry", "option_symbol"],
    primary_key="id",
    unique_key="option_symbol"
)

option_prices_schema = OptionTableSchema(
    name="option_prices",
    columns=[
        "id", "option_id", "timestamp", "spot_price", "bid", "bid_size", "ask", "ask_size",
        "last", "volume", "oi", "iv", "delta", "gamma", "theta", "vega", "rho",
        "source", "model_price", "iv_bid", "iv_ask", "incomplete", "anomaly_score"
    ],
    primary_key="id"
)