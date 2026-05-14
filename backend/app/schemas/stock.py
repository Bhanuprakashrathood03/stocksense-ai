from pydantic import BaseModel
from datetime import datetime


class StockSearchResult(BaseModel):
    symbol: str
    name: str
    exchange: str
    type: str


class StockQuote(BaseModel):
    symbol: str
    price: float
    change: float
    change_pct: float
    volume: int
    high_52w: float | None = None
    low_52w: float | None = None


class StockHistory(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class SignalResponse(BaseModel):
    symbol: str
    signal_type: str
    price: float
    confidence: float
    reason: str | None
    created_at: datetime
