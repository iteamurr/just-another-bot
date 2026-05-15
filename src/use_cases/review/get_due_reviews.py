from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from src.domain.review.dao import ReviewCardDAO
from src.domain.review.entities import ReviewCard


@dataclass(frozen=True, slots=True, kw_only=True)
class GetDueReviewsResult:
    cards: list[ReviewCard]
    total_due: int


@dataclass(frozen=True, slots=True, kw_only=True)
class GetDueReviewsUseCase:
    review_card_dao: ReviewCardDAO

    async def execute(self, *, limit: int = 20) -> GetDueReviewsResult:
        now = datetime.now(tz=UTC)
        cards = await self.review_card_dao.list_due(now=now, limit=limit)
        total = await self.review_card_dao.count_due(now=now)
        return GetDueReviewsResult(cards=cards, total_due=total)
