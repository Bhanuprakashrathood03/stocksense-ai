from pydantic import BaseModel
from datetime import datetime


class AlertCreate(BaseModel):
    symbol: str
    condition: str
    threshold: float


class AlertResponse(BaseModel):
    id: str
    symbol: str
    condition: str
    threshold: float
    triggered: bool
    active: bool
    created_at: datetime

    class Config:
        from_attributes = True
