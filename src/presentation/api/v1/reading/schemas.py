from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from src.domain.pagination import Pagination
from src.domain.reading.entities import ReadingItem
from src.use_cases.reading.get_reading_stats import ReadingStatsResult
from src.use_cases.reading.list_reading_items import ListReadingItemsResult


class ReadingSourceSchema(BaseModel):
    kind: str
    url: str | None = None


class LogReadingItemRequest(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    source_kind: str
    source_url: str | None = None
    takeaway: str
    tags: list[str] = Field(default_factory=list)
    finished_at: datetime | None = None


class ReadingItemResponse(BaseModel):
    id: str
    title: str
    source: ReadingSourceSchema
    takeaway: str
    tags: list[str]
    finished_at: datetime | None
    created_at: datetime

    @classmethod
    def from_domain(cls, item: ReadingItem) -> ReadingItemResponse:
        return cls(
            id=item.id,
            title=item.title,
            source=ReadingSourceSchema(kind=item.source.kind.value, url=item.source.url),
            takeaway=item.takeaway.text,
            tags=item.tags,
            finished_at=item.finished_at,
            created_at=item.created_at,
        )


class ListReadingItemsResponse(BaseModel):
    items: list[ReadingItemResponse]
    total: int
    limit: int
    offset: int

    @classmethod
    def from_domain(cls, result: ListReadingItemsResult, *, pagination: Pagination) -> ListReadingItemsResponse:
        return cls(
            items=[ReadingItemResponse.from_domain(i) for i in result.items],
            total=result.total,
            limit=pagination.limit,
            offset=pagination.offset,
        )


class WeekCountSchema(BaseModel):
    week: str
    count: int


class TagCountSchema(BaseModel):
    tag: str
    count: int


class ReadingStatsResponse(BaseModel):
    total_items: int
    by_week: list[WeekCountSchema]
    by_tag: list[TagCountSchema]

    @classmethod
    def from_domain(cls, result: ReadingStatsResult) -> ReadingStatsResponse:
        return cls(
            total_items=result.total_items,
            by_week=[WeekCountSchema(**row) for row in result.by_week],
            by_tag=[TagCountSchema(**row) for row in result.by_tag],
        )
