from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.review.dao import ReviewHistoryDAO
from src.domain.review.entities import ReviewHistoryEntry
from src.infrastructure.database.mappers import review_history_mapper
from src.infrastructure.database.models.review_history import ReviewHistoryModel


class SqlAlchemyReviewHistoryDAO(ReviewHistoryDAO):
    def __init__(self, *, session: AsyncSession) -> None:
        self._session = session

    async def append(self, entry: ReviewHistoryEntry) -> ReviewHistoryEntry:
        model = review_history_mapper.review_history_entry_to_model(entry)
        self._session.add(model)
        await self._session.flush()
        return entry

    async def list_by_card(self, card_id: str) -> list[ReviewHistoryEntry]:
        sql = text(
            "SELECT * FROM review_history"
            " WHERE card_id = :card_id"
            " ORDER BY reviewed_at DESC"
        )
        result = await self._session.execute(sql, {"card_id": card_id})
        rows = result.mappings().all()
        models = [ReviewHistoryModel(**dict(row)) for row in rows]
        return [review_history_mapper.model_to_review_history_entry(m) for m in models]
