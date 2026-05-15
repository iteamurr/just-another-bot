from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.reading.dao import ReadingItemDAO
from src.domain.reading.entities import ReadingItem
from src.infrastructure.database.mappers import reading_item_mapper
from src.infrastructure.database.models.reading_item import ReadingItemModel


class SqlAlchemyReadingItemDAO(ReadingItemDAO):
    def __init__(self, *, session: AsyncSession) -> None:
        self._session = session

    async def save(self, item: ReadingItem) -> ReadingItem:
        model = reading_item_mapper.reading_item_to_model(item)
        existing = await self._session.get(ReadingItemModel, item.id)
        if existing is None:
            self._session.add(model)
        else:
            await self._session.merge(model)
        await self._session.flush()
        return item

    async def get_by_id(self, item_id: str) -> ReadingItem | None:
        model = await self._session.get(ReadingItemModel, item_id)
        if model is None:
            return None
        return reading_item_mapper.model_to_reading_item(model)

    async def list(
        self,
        *,
        tag: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[ReadingItem]:
        query = self._session.query(ReadingItemModel).order_by(ReadingItemModel.created_at.desc())
        if tag is not None:
            query = query.where(ReadingItemModel.tags.contains([tag]))
        query = query.limit(limit).offset(offset)
        result = await self._session.execute(query)
        return [reading_item_mapper.model_to_reading_item(m) for m in result.scalars()]

    async def count(self, *, tag: str | None = None) -> int:
        query = self._session.query(func.count()).select_from(ReadingItemModel)
        if tag is not None:
            query = query.where(ReadingItemModel.tags.contains([tag]))
        result = await self._session.execute(query)
        return int(result.scalar_one())

    async def count_by_week(self) -> list[dict[str, int]]:
        cutoff = datetime.now(tz=UTC) - timedelta(weeks=12)
        week_expr = func.date_trunc("week", ReadingItemModel.created_at)
        query = (
            self._session.query(week_expr.label("week"), func.count().label("count"))
            .where(ReadingItemModel.created_at >= cutoff)
            .group_by(week_expr)
            .order_by(week_expr)
        )
        result = await self._session.execute(query)
        return [{"week": str(row.week), "count": row.count} for row in result]

    async def count_by_tag(self) -> list[dict[str, int]]:
        tag_col = func.unnest(ReadingItemModel.tags).column_valued("tag")
        query = (
            self._session.query(tag_col, func.count().label("count")).group_by(tag_col).order_by(func.count().desc())
        )
        result = await self._session.execute(query)
        return [{"tag": row.tag, "count": row.count} for row in result]
