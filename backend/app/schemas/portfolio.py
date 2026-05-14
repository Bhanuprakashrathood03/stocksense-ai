from pydantic import BaseModel
from datetime import datetime


class PortfolioCreate(BaseModel):
    name: str
    risk_profile: str = "moderate"
    cash_balance: float = 0.0


class PortfolioResponse(BaseModel):
    id: str
    name: str
    risk_profile: str
    total_value: float
    cash_balance: float
    created_at: datetime
    holdings: list["HoldingResponse"] = []

    class Config:
        from_attributes = True


class HoldingCreate(BaseModel):
    symbol: str
    quantity: float
    avg_price: float


class HoldingResponse(BaseModel):
    id: str
    symbol: str
    quantity: float
    avg_price: float
    current_price: float | None

    class Config:
        from_attributes = True


class WatchlistResponse(BaseModel):
    id: str
    symbol: str
    added_at: datetime

    class Config:
        from_attributes = True
