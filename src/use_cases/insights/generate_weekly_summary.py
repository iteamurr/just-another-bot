from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from src.domain.llm.client import LLMClient
from src.domain.reading.dao import ReadingItemDAO
from src.domain.transaction import ITransactionContext


@dataclass(frozen=True, slots=True, kw_only=True)
class GenerateWeeklySummaryResult:
    summary: str
    items_count: int


@dataclass(frozen=True, slots=True, kw_only=True)
class GenerateWeeklySummaryUseCase:
    transaction_context: ITransactionContext
    reading_item_dao: ReadingItemDAO
    llm_client: LLMClient

    async def execute(self) -> GenerateWeeklySummaryResult:
        async with self.transaction_context:
            items = await self.reading_item_dao.list(limit=200, offset=0)
            cutoff = datetime.now(tz=UTC) - timedelta(days=7)
            recent = [i for i in items if i.created_at and i.created_at >= cutoff]

            if not recent:
                return GenerateWeeklySummaryResult(
                    summary="За последнюю неделю ничего не добавлено",
                    items_count=0,
                )

            summary = await self.llm_client.generate_weekly_summary(items=recent)
            return GenerateWeeklySummaryResult(summary=summary, items_count=len(recent))
