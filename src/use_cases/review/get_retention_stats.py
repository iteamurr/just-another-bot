from __future__ import annotations

from dataclasses import dataclass

from src.domain.review.dao import ReviewCardDAO
from src.domain.transaction import ITransactionContext


@dataclass(frozen=True, slots=True, kw_only=True)
class RetentionStatsResult:
    overall_retention: float
    avg_ease_factor: float
    total_reviews: int


@dataclass(frozen=True, slots=True, kw_only=True)
class GetRetentionStatsUseCase:
    transaction_context: ITransactionContext
    review_card_dao: ReviewCardDAO

    async def execute(self) -> RetentionStatsResult:
        async with self.transaction_context:
            stats = await self.review_card_dao.retention_stats()
            return RetentionStatsResult(
                overall_retention=stats.overall_retention,
                avg_ease_factor=stats.avg_ease_factor,
                total_reviews=stats.total_reviews,
            )
