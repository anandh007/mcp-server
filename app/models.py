from pydantic import BaseModel
from typing import Any, Dict

class TickerResponse(BaseModel):
    exchange: str
    symbol: str
    data: Dict[str, Any]

class OHLCVRequest(BaseModel):
    exchange: str
    symbol: str
    timeframe: str = "1m"
    limit: int = 100
