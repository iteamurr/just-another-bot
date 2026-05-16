from __future__ import annotations

from datetime import datetime
from typing import cast

from sqlalchemy import Numeric, case, func, select

from src.domain.review.dao import RetentionStats, ReviewCardDAO
from src.domain.review.entities import ReviewCard
from src.infrastructure.database.dao.base import BaseDAO
from src.infrastructure.database.models.review_card import ReviewCardModel
from src.infrastructure.database.models.review_history import ReviewHistoryModel


class SqlAlchemyReviewCardDAO(BaseDAO, ReviewCardDAO):
    async def save(self, card: ReviewCard) -> ReviewCard:
        await self.session.merge(ReviewCardModel.from_domain(card))
        await self.session.flush()
        return card

    async def get_by_id(self, card_id: str) -> ReviewCard | None:
        model: ReviewCardModel | None = await self.session.get(ReviewCardModel, card_id)
        if model is None:
            return None
        return model.to_domain()

    async def get_by_item_id(self, item_id: str) -> ReviewCard | None:
        stmt = select(ReviewCardModel).where(ReviewCardModel.item_id == item_id).limit(1)
        result = await self.session.execute(stmt)
        model: ReviewCardModel | None = result.scalar_one_or_none()
        if model is None:
            return None
        return model.to_domain()

    async def list_due(self, *, now: datetime, limit: int = 20) -> list[ReviewCard]:
        stmt = (
            select(ReviewCardModel)
            .where(ReviewCardModel.due_at <= now)
            .order_by(ReviewCardModel.due_at.asc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return [cast(ReviewCardModel, m).to_domain() for m in result.scalars()]

    async def count_due(self, *, now: datetime) -> int:
        stmt = select(func.count()).select_from(ReviewCardModel).where(ReviewCardModel.due_at <= now)
        result = await self.session.execute(stmt)
        return int(result.scalar_one())

    async def retention_stats(self) -> RetentionStats:
        stmt = select(
            func.round(
                func.avg(case((ReviewHistoryModel.grade >= 3, 1.0), else_=0.0)).cast(Numeric),
                4,
            ).label("overall_retention"),
            func.round(func.avg(ReviewHistoryModel.ease_factor_after).cast(Numeric), 4).label("avg_ease_factor"),
            func.count().label("total_reviews"),
        )
        result = await self.session.execute(stmt)
        row = result.mappings().first()
        if row is None:
            return RetentionStats(overall_retention=0.0, avg_ease_factor=2.5, total_reviews=0)
        return RetentionStats(
            overall_retention=float(row["overall_retention"] or 0),
            avg_ease_factor=float(row["avg_ease_factor"] or 2.5),
            total_reviews=int(row["total_reviews"]),
        )
