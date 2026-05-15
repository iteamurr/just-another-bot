from sqlalchemy import Column, DateTime, Float, Index, Integer, String, Text

from src.infrastructure.database.models.base import Base


class ReviewCardModel(Base):
    __tablename__ = "review_cards"
    __table_args__ = (
        Index("ix_review_cards_item_id", "item_id"),
        Index("ix_review_cards_due_at", "due_at"),
    )

    id = Column(String(36), primary_key=True, nullable=False)
    item_id = Column(String(36), nullable=False)
    ease_factor = Column(Float, nullable=False)
    interval_days = Column(Integer, nullable=False)
    repetitions = Column(Integer, nullable=False)
    due_at = Column(DateTime(timezone=True), nullable=False)
    cached_question = Column(Text, nullable=True)
