from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ReviewCardResponse(BaseModel):
    id: str
    item_id: str
    ease_factor: float
    interval_days: int
    repetitions: int
    due_at: datetime
    cached_question: str | None


class DueReviewsResponse(BaseModel):
    cards: list[ReviewCardResponse]
    total_due: int


class ReviewQuestionResponse(BaseModel):
    card_id: str
    question: str


class SubmitGradeRequest(BaseModel):
    grade: int = Field(ge=0, le=5)


class SubmitGradeResponse(BaseModel):
    card_id: str
    new_interval_days: int
    new_ease_factor: float
    due_at: datetime


class RetentionStatsResponse(BaseModel):
    overall_retention: float
    avg_ease_factor: float
    total_reviews: int
