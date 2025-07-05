from tradx.backend.quant.seasonality_score import SeasonalityScore
from tradx.backend import stock
from pydantic import BaseModel
from tradx.backend.quant.momentum_score import MomentumScore
from typing import Optional

class QScore(BaseModel):
    stock:stock
    momentum:MomentumScore
    seasonality:SeasonalityScore

    volatility:float
    options:float

    def __init__(self) -> None:
        pass
