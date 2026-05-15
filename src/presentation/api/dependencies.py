from __future__ import annotations

from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.container import container
from src.domain.llm.client import LLMClient
from src.domain.reading.dao import ReadingItemDAO
from src.domain.review.dao import ReviewCardDAO, ReviewHistoryDAO
from src.infrastructure.database.dao.reading_item_dao import SqlAlchemyReadingItemDAO
from src.infrastructure.database.dao.review_card_dao import SqlAlchemyReviewCardDAO
from src.infrastructure.database.dao.review_history_dao import SqlAlchemyReviewHistoryDAO


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Сессия с автоматическим управлением транзакцией на запрос"""
    factory: async_sessionmaker[AsyncSession] = container.resolve(async_sessionmaker)
    async with factory() as session:
        async with session.begin():
            yield session


def get_reading_item_dao(
    session: AsyncSession = Depends(get_db_session),
) -> ReadingItemDAO:
    return SqlAlchemyReadingItemDAO(session=session)


def get_review_card_dao(
    session: AsyncSession = Depends(get_db_session),
) -> ReviewCardDAO:
    return SqlAlchemyReviewCardDAO(session=session)


def get_review_history_dao(
    session: AsyncSession = Depends(get_db_session),
) -> ReviewHistoryDAO:
    return SqlAlchemyReviewHistoryDAO(session=session)


def get_llm_client() -> LLMClient:
    return container.resolve(LLMClient)
