from __future__ import annotations

from sqlalchemy import text
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
        # фильтр по тегу опциональный — строим запрос динамически
        if tag is not None:
            sql = text(
                "SELECT * FROM reading_items"
                " WHERE :tag = ANY(tags)"
                " ORDER BY created_at DESC"
                " LIMIT :limit OFFSET :offset"
            )
            params: dict[str, object] = {"tag": tag, "limit": limit, "offset": offset}
        else:
            sql = text(
                "SELECT * FROM reading_items"
                " ORDER BY created_at DESC"
                " LIMIT :limit OFFSET :offset"
            )
            params = {"limit": limit, "offset": offset}

        result = await self._session.execute(sql, params)
        rows = result.mappings().all()
        models = [ReadingItemModel(**dict(row)) for row in rows]
        return [reading_item_mapper.model_to_reading_item(m) for m in models]

    async def count(self, *, tag: str | None = None) -> int:
        if tag is not None:
            sql = text("SELECT COUNT(*) FROM reading_items WHERE :tag = ANY(tags)")
            result = await self._session.execute(sql, {"tag": tag})
        else:
            sql = text("SELECT COUNT(*) FROM reading_items")
            result = await self._session.execute(sql)
        return int(result.scalar_one())

    async def count_by_week(self) -> list[dict[str, int]]:
        sql = text("""
            SELECT date_trunc('week', created_at) AS week, COUNT(*)::int AS count
            FROM reading_items
            WHERE created_at >= now() - interval '12 weeks'
            GROUP BY 1 ORDER BY 1
        """)
        result = await self._session.execute(sql)
        return [{"week": str(row.week), "count": row.count} for row in result]

    async def count_by_tag(self) -> list[dict[str, int]]:
        sql = text("""
            SELECT tag, COUNT(*)::int AS count
            FROM reading_items, unnest(tags) AS tag
            GROUP BY tag ORDER BY count DESC
        """)
        result = await self._session.execute(sql)
        return [{"tag": row.tag, "count": row.count} for row in result]
