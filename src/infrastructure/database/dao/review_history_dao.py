from __future__ import annotations

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
        query = (
            self._session.query(ReviewHistoryModel)
            .where(ReviewHistoryModel.card_id == card_id)
            .order_by(ReviewHistoryModel.reviewed_at.desc())
        )
        result = await self._session.execute(query)
        return [review_history_mapper.model_to_review_history_entry(m) for m in result.scalars()]
