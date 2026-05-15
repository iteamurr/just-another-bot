from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Self

from src.domain.review.dao import ReviewCardDAO, ReviewHistoryDAO
from src.domain.review.entities import ReviewCard, ReviewHistoryEntry
from src.domain.review.exceptions import ReviewCardNotFoundException
from src.domain.review.value_objects import Grade


@dataclass(frozen=True, slots=True, kw_only=True)
class SubmitReviewGradeCommand:
    card_id: str
    grade: Grade

    @classmethod
    def new(cls, *, card_id: str, grade: int) -> Self:
        return cls(card_id=card_id, grade=Grade(value=grade))


@dataclass(frozen=True, slots=True, kw_only=True)
class SubmitReviewGradeResult:
    card: ReviewCard
    history_entry: ReviewHistoryEntry


@dataclass(frozen=True, slots=True, kw_only=True)
class SubmitReviewGradeUseCase:
    review_card_dao: ReviewCardDAO
    review_history_dao: ReviewHistoryDAO

    async def execute(self, command: SubmitReviewGradeCommand) -> SubmitReviewGradeResult:
        card = await self.review_card_dao.get_by_id(command.card_id)
        if card is None:
            raise ReviewCardNotFoundException(card_id=command.card_id)

        now = datetime.now(tz=UTC)
        card.apply_grade(command.grade, now)

        entry = ReviewHistoryEntry(
            card_id=card.id,
            grade=command.grade.value,
            ease_factor_after=card.ease_factor.value,
            interval_days_after=card.interval_days,
            reviewed_at=now,
        )

        saved_card = await self.review_card_dao.save(card)
        saved_entry = await self.review_history_dao.append(entry)

        return SubmitReviewGradeResult(card=saved_card, history_entry=saved_entry)
