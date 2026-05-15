from __future__ import annotations

from datetime import datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.review.dao import ReviewCardDAO
from src.domain.review.entities import ReviewCard
from src.infrastructure.database.mappers import review_card_mapper
from src.infrastructure.database.models.review_card import ReviewCardModel


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
        sql = text("SELECT * FROM review_cards WHERE item_id = :item_id LIMIT 1")
        result = await self._session.execute(sql, {"item_id": item_id})
        row = result.mappings().first()
        if row is None:
            return None
        return review_card_mapper.model_to_review_card(ReviewCardModel(**dict(row)))

    async def list_due(self, *, now: datetime, limit: int = 20) -> list[ReviewCard]:
        sql = text("SELECT * FROM review_cards" " WHERE due_at <= :now" " ORDER BY due_at ASC" " LIMIT :limit")
        result = await self._session.execute(sql, {"now": now, "limit": limit})
        rows = result.mappings().all()
        models = [ReviewCardModel(**dict(row)) for row in rows]
        return [review_card_mapper.model_to_review_card(m) for m in models]

    async def count_due(self, *, now: datetime) -> int:
        sql = text("SELECT COUNT(*) FROM review_cards WHERE due_at <= :now")
        result = await self._session.execute(sql, {"now": now})
        return int(result.scalar_one())

    async def retention_stats(self) -> dict[str, float]:
        sql = text("""
            SELECT
                ROUND(AVG(CASE WHEN grade >= 3 THEN 1.0 ELSE 0.0 END)::numeric, 4) AS overall_retention,
                ROUND(AVG(ease_factor_after)::numeric, 4)                           AS avg_ease_factor,
                COUNT(*)                                                             AS total_reviews
            FROM review_history
        """)
        result = await self._session.execute(sql)
        row = result.mappings().first()
        if row is None:
            return {"overall_retention": 0.0, "avg_ease_factor": 2.5, "total_reviews": 0.0}
        return {
            "overall_retention": float(row["overall_retention"] or 0),
            "avg_ease_factor": float(row["avg_ease_factor"] or 2.5),
            "total_reviews": float(row["total_reviews"]),
        }
