from __future__ import annotations

from sqlalchemy import Column, DateTime, Float, Index, Integer, String

from src.domain.review.entities import ReviewHistoryEntry
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

    @classmethod
    def from_domain(cls, entry: ReviewHistoryEntry) -> ReviewHistoryModel:
        return cls(
            id=entry.id,
            card_id=entry.card_id,
            grade=entry.grade,
            ease_factor_after=entry.ease_factor_after,
            interval_days_after=entry.interval_days_after,
            reviewed_at=entry.reviewed_at,
        )

    def to_domain(self) -> ReviewHistoryEntry:
        return ReviewHistoryEntry(
            id=self.id,
            card_id=self.card_id,
            grade=self.grade,
            ease_factor_after=self.ease_factor_after,
            interval_days_after=self.interval_days_after,
            reviewed_at=self.reviewed_at,  # type: ignore[arg-type]
        )
