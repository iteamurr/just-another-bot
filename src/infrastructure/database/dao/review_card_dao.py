from __future__ import annotations

from datetime import datetime

from sqlalchemy import Numeric, case, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.review.dao import ReviewCardDAO
from src.domain.review.entities import ReviewCard
from src.infrastructure.database.mappers import review_card_mapper
from src.infrastructure.database.models.review_card import ReviewCardModel
from src.infrastructure.database.models.review_history import ReviewHistoryModel


class SqlAlchemyReviewCardDAO(ReviewCardDAO):
    def __init__(self, *, session: AsyncSession) -> None:
        self._session = session

    async def save(self, card: ReviewCard) -> ReviewCard:
        model = review_card_mapper.review_card_to_model(card)
        existing = await self._session.get(ReviewCardModel, card.id)
        if existing is None:
            self._session.add(model)
        else:
            await self._session.merge(model)
        await self._session.flush()
        return card

    async def get_by_id(self, card_id: str) -> ReviewCard | None:
        model = await self._session.get(ReviewCardModel, card_id)
        if model is None:
            return None
        return review_card_mapper.model_to_review_card(model)

    async def get_by_item_id(self, item_id: str) -> ReviewCard | None:
        query = self._session.query(ReviewCardModel).where(ReviewCardModel.item_id == item_id).limit(1)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return review_card_mapper.model_to_review_card(model)

    async def list_due(self, *, now: datetime, limit: int = 20) -> list[ReviewCard]:
        query = (
            self._session.query(ReviewCardModel)
            .where(ReviewCardModel.due_at <= now)
            .order_by(ReviewCardModel.due_at.asc())
            .limit(limit)
        )
        result = await self._session.execute(query)
        return [review_card_mapper.model_to_review_card(m) for m in result.scalars()]

    async def count_due(self, *, now: datetime) -> int:
        query = self._session.query(func.count()).select_from(ReviewCardModel).where(ReviewCardModel.due_at <= now)
        result = await self._session.execute(query)
        return int(result.scalar_one())

    async def retention_stats(self) -> dict[str, float]:
        query = self._session.query(
            func.round(
                func.avg(case((ReviewHistoryModel.grade >= 3, 1.0), else_=0.0)).cast(Numeric),
                4,
            ).label("overall_retention"),
            func.round(func.avg(ReviewHistoryModel.ease_factor_after).cast(Numeric), 4).label("avg_ease_factor"),
            func.count().label("total_reviews"),
        )
        result = await self._session.execute(query)
        row = result.mappings().first()
        if row is None:
            return {"overall_retention": 0.0, "avg_ease_factor": 2.5, "total_reviews": 0.0}
        return {
            "overall_retention": float(row["overall_retention"] or 0),
            "avg_ease_factor": float(row["avg_ease_factor"] or 2.5),
            "total_reviews": float(row["total_reviews"]),
        }
