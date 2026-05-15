from __future__ import annotations

from dataclasses import dataclass

from src.domain.review.dao import ReviewCardDAO


@dataclass(frozen=True, slots=True, kw_only=True)
class RetentionStatsResult:
    overall_retention: float
    avg_ease_factor: float
    total_reviews: int


@dataclass(frozen=True, slots=True, kw_only=True)
class GetRetentionStatsUseCase:
    review_card_dao: ReviewCardDAO

    async def execute(self) -> RetentionStatsResult:
        stats = await self.review_card_dao.retention_stats()
        return RetentionStatsResult(
            overall_retention=stats["overall_retention"],
            avg_ease_factor=stats["avg_ease_factor"],
            total_reviews=int(stats["total_reviews"]),
        )
