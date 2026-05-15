from sqlalchemy import Column, DateTime, Float, Index, Integer, String

from src.infrastructure.database.models.base import Base


class ReviewHistoryModel(Base):
    __tablename__ = "review_history"
    __table_args__ = (Index("ix_review_history_card_id", "card_id"),)

    id = Column(String(36), primary_key=True, nullable=False)
    card_id = Column(String(36), nullable=False)
    grade = Column(Integer, nullable=False)
    ease_factor_after = Column(Float, nullable=False)
    interval_days_after = Column(Integer, nullable=False)
    reviewed_at = Column(DateTime(timezone=True), nullable=False)
