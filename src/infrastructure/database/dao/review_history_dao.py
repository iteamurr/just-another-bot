from __future__ import annotations

from typing import cast

from src.domain.review.dao import ReviewHistoryDAO
from src.domain.review.entities import ReviewHistoryEntry
from src.infrastructure.database.dao.base import BaseDAO
from src.infrastructure.database.models.review_history import ReviewHistoryModel


class SqlAlchemyReviewHistoryDAO(BaseDAO, ReviewHistoryDAO):
    async def append(self, entry: ReviewHistoryEntry) -> ReviewHistoryEntry:
        model = ReviewHistoryModel.from_domain(entry)
        self.session.add(model)
        await self.session.flush()
        return entry

    async def list_by_card(self, card_id: str) -> list[ReviewHistoryEntry]:
        query = (
            self.session.query(ReviewHistoryModel)
            .where(ReviewHistoryModel.card_id == card_id)
            .order_by(ReviewHistoryModel.reviewed_at.desc())
        )
        result = await self.session.execute(query)
        return [cast(ReviewHistoryModel, m).to_domain() for m in result.scalars()]
