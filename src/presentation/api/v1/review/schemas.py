from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from src.domain.review.entities import ReviewCard
    from src.use_cases.review.generate_review_question import GenerateReviewQuestionResult
    from src.use_cases.review.get_due_reviews import GetDueReviewsResult
    from src.use_cases.review.get_retention_stats import RetentionStatsResult


class ReviewCardResponse(BaseModel):
    id: str
    item_id: str
    ease_factor: float
    interval_days: int
    repetitions: int
    due_at: datetime
    cached_question: str | None

    @classmethod
    def from_domain(cls, card: ReviewCard) -> ReviewCardResponse:
        return cls(
            id=card.id,
            item_id=card.item_id,
            ease_factor=card.ease_factor.value,
            interval_days=card.interval_days,
            repetitions=card.repetitions,
            due_at=card.due_at,
            cached_question=card.cached_question,
        )


class DueReviewsResponse(BaseModel):
    cards: list[ReviewCardResponse]
    total_due: int

    @classmethod
    def from_domain(cls, result: GetDueReviewsResult) -> DueReviewsResponse:
        return cls(
            cards=[ReviewCardResponse.from_domain(c) for c in result.cards],
            total_due=result.total_due,
        )


class ReviewQuestionResponse(BaseModel):
    card_id: str
    question: str

    @classmethod
    def from_domain(cls, result: GenerateReviewQuestionResult) -> ReviewQuestionResponse:
        return cls(card_id=result.card_id, question=result.question)


class SubmitGradeRequest(BaseModel):
    grade: int = Field(ge=0, le=5)


class SubmitGradeResponse(BaseModel):
    card_id: str
    new_interval_days: int
    new_ease_factor: float
    due_at: datetime

    @classmethod
    def from_domain(cls, card: ReviewCard) -> SubmitGradeResponse:
        return cls(
            card_id=card.id,
            new_interval_days=card.interval_days,
            new_ease_factor=card.ease_factor.value,
            due_at=card.due_at,
        )


class RetentionStatsResponse(BaseModel):
    overall_retention: float
    avg_ease_factor: float
    total_reviews: int

    @classmethod
    def from_domain(cls, result: RetentionStatsResult) -> RetentionStatsResponse:
        return cls(
            overall_retention=result.overall_retention,
            avg_ease_factor=result.avg_ease_factor,
            total_reviews=result.total_reviews,
        )
