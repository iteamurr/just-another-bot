from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from src.domain.reading.dao import ReadingItemDAO
from src.domain.reading.entities import ReadingItem
from src.domain.transaction import ITransactionContext


@dataclass(frozen=True, slots=True, kw_only=True)
class ListReadingItemsQuery:
    tag: str | None
    limit: int
    offset: int

    @classmethod
    def new(cls, *, tag: str | None = None, limit: int = 20, offset: int = 0) -> Self:
        return cls(tag=tag, limit=limit, offset=offset)


@dataclass(frozen=True, slots=True, kw_only=True)
class ListReadingItemsResult:
    items: list[ReadingItem]
    total: int


@dataclass(frozen=True, slots=True, kw_only=True)
class ListReadingItemsUseCase:
    transaction_context: ITransactionContext
    reading_item_dao: ReadingItemDAO

    async def execute(self, query: ListReadingItemsQuery) -> ListReadingItemsResult:
        async with self.transaction_context:
            items = await self.reading_item_dao.list(tag=query.tag, limit=query.limit, offset=query.offset)
            total = await self.reading_item_dao.count(tag=query.tag)
            return ListReadingItemsResult(items=items, total=total)
