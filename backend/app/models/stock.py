import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum
from ..core.database import Base


class SignalType(str, enum.Enum):
    buy = "buy"
    sell = "sell"
    hold = "hold"
    strong_buy = "strong_buy"
    strong_sell = "strong_sell"


class StockSignal(Base):
    __tablename__ = "stock_signals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    symbol: Mapped[str] = mapped_column(String(10), index=True, nullable=False)
    signal_type: Mapped[SignalType] = mapped_column(SAEnum(SignalType), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    reason: Mapped[str] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
