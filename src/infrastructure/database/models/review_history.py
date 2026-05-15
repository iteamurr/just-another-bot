from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import Base


class ReviewHistoryModel(Base):
    __tablename__ = "review_history"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    card_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    ease_factor_after: Mapped[float] = mapped_column(Float, nullable=False)
    interval_days_after: Mapped[int] = mapped_column(Integer, nullable=False)
    reviewed_at: Mapped[str] = mapped_column(DateTime(timezone=True), nullable=False)
