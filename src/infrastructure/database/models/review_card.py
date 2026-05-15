from __future__ import annotations

from sqlalchemy import Column, DateTime, Float, Index, Integer, String, Text

from src.domain.review.entities import ReviewCard
from src.domain.review.value_objects import EaseFactor
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

    @classmethod
    def from_domain(cls, card: ReviewCard) -> ReviewCardModel:
        return cls(
            id=card.id,
            item_id=card.item_id,
            ease_factor=card.ease_factor.value,
            interval_days=card.interval_days,
            repetitions=card.repetitions,
            due_at=card.due_at,
            cached_question=card.cached_question,
        )

    def to_domain(self) -> ReviewCard:
        return ReviewCard(
            id=self.id,
            item_id=self.item_id,
            ease_factor=EaseFactor(value=self.ease_factor),
            interval_days=self.interval_days,
            repetitions=self.repetitions,
            due_at=self.due_at,  # type: ignore[arg-type]
            cached_question=self.cached_question,
        )
