from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Self

from src.domain.reading.dao import ReadingItemDAO
from src.domain.reading.entities import ReadingItem
from src.domain.reading.value_objects import ReadingSource, SourceKind, Takeaway
from src.domain.review.dao import ReviewCardDAO
from src.domain.review.entities import ReviewCard
from src.domain.transaction import ITransactionContext


@dataclass(frozen=True, slots=True, kw_only=True)
class LogReadingItemCommand:
    title: str
    source: ReadingSource
    takeaway: Takeaway
    tags: tuple[str, ...]
    finished_at: datetime | None

    @classmethod
    def new(
        cls,
        *,
        title: str,
        source_kind: str,
        source_url: str | None = None,
        takeaway: str,
        tags: list[str] | None = None,
        finished_at: datetime | None = None,
    ) -> Self:
        return cls(
            title=title,
            source=ReadingSource(kind=SourceKind(source_kind), url=source_url),
            takeaway=Takeaway(text=takeaway),
            tags=tuple(tags or []),
            finished_at=finished_at,
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class LogReadingItemResult:
    item: ReadingItem
    card: ReviewCard


@dataclass(frozen=True, slots=True, kw_only=True)
class LogReadingItemUseCase:
    transaction_context: ITransactionContext
    reading_item_dao: ReadingItemDAO
    review_card_dao: ReviewCardDAO

    async def execute(self, command: LogReadingItemCommand) -> LogReadingItemResult:
        async with self.transaction_context:
            item = ReadingItem(
                title=command.title,
                source=command.source,
                takeaway=command.takeaway,
                tags=list(command.tags),
                finished_at=command.finished_at,
                created_at=datetime.now(tz=UTC),
            )
            card = ReviewCard(item_id=item.id, due_at=datetime.now(tz=UTC))
            saved_item = await self.reading_item_dao.save(item)
            saved_card = await self.review_card_dao.save(card)
            return LogReadingItemResult(item=saved_item, card=saved_card)
