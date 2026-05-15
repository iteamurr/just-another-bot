from __future__ import annotations

from dataclasses import dataclass

from src.domain.reading.dao import ReadingItemDAO


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadingStatsResult:
    total_items: int
    by_week: list[dict[str, int]]
    by_tag: list[dict[str, int]]


@dataclass(frozen=True, slots=True, kw_only=True)
class GetReadingStatsUseCase:
    reading_item_dao: ReadingItemDAO

    async def execute(self) -> ReadingStatsResult:
        total = await self.reading_item_dao.count()
        by_week = await self.reading_item_dao.count_by_week()
        by_tag = await self.reading_item_dao.count_by_tag()
        return ReadingStatsResult(total_items=total, by_week=by_week, by_tag=by_tag)
