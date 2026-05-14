from pydantic import BaseModel
from datetime import datetime


class SubscriptionResponse(BaseModel):
    id: str
    plan: str
    status: str
    renews_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True


class UpgradeRequest(BaseModel):
    plan: str
