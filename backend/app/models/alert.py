import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, Float, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from ..core.database import Base


class AlertCondition(str, enum.Enum):
    above = "above"
    below = "below"
    cross_above = "cross_above"
    cross_below = "cross_below"
    volume_spike = "volume_spike"
    price_change = "price_change"


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    symbol: Mapped[str] = mapped_column(String(10), nullable=False)
    condition: Mapped[AlertCondition] = mapped_column(SAEnum(AlertCondition), nullable=False)
    threshold: Mapped[float] = mapped_column(Float, nullable=False)
    triggered: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="alerts")
