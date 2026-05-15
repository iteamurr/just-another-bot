from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


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


class ListReadingItemsResponse(BaseModel):
    items: list[ReadingItemResponse]
    total: int
    limit: int
    offset: int


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
