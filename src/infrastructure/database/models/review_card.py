from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import Base


class ReviewCardModel(Base):
    __tablename__ = "review_cards"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    item_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    ease_factor: Mapped[float] = mapped_column(Float, nullable=False)
    interval_days: Mapped[int] = mapped_column(Integer, nullable=False)
    repetitions: Mapped[int] = mapped_column(Integer, nullable=False)
    due_at: Mapped[str] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    cached_question: Mapped[str | None] = mapped_column(Text, nullable=True)
