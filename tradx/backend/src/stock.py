from pydantic import BaseModel, HttpUrl, Field
from typing import Optional


class Stock(BaseModel):
    symbol: str
    name: str
    isin: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[HttpUrl] = None
    ir_website: Optional[HttpUrl] = None
    long_summary: Optional[str] = None
    employees: Optional[int] = None

    market_cap: Optional[float] = None
    current_price: Optional[float] = None
    dividend_yield: Optional[float] = None
    pe_ratio: Optional[float] = None
    beta: Optional[float] = None

    fifty_two_week_high: Optional[float] = Field(None, alias="52wHigh")
    fifty_two_week_low: Optional[float] = Field(None, alias="52wLow")
    average_volume: Optional[int] = None

    currency: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None

    def is_valid(self) -> bool:
        return self.symbol is not None and self.name is not None