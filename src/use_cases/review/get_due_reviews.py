from __future__ import annotations

from dataclasses import dataclass

from src.domain.datetime_provider import IDateTimeProvider
from src.domain.review.dao import ReviewCardDAO
from src.domain.review.entities import ReviewCard
from src.domain.transaction import ITransactionContext


@dataclass(frozen=True, slots=True, kw_only=True)
class GetDueReviewsResult:
    cards: list[ReviewCard]
    total_due: int


@dataclass(frozen=True, slots=True, kw_only=True)
class GetDueReviewsUseCase:
    transaction_context: ITransactionContext
    datetime_provider: IDateTimeProvider
    review_card_dao: ReviewCardDAO

    async def execute(self, *, limit: int = 20) -> GetDueReviewsResult:
        async with self.transaction_context:
            now = self.datetime_provider.now()
            cards = await self.review_card_dao.list_due(now=now, limit=limit)
            total = await self.review_card_dao.count_due(now=now)
            return GetDueReviewsResult(cards=cards, total_due=total)
