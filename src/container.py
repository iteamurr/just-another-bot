from __future__ import annotations

from contextvars import ContextVar

import httpx
import punq
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.llm.client import LLMClient
from src.domain.reading.dao import ReadingItemDAO
from src.domain.review.dao import ReviewCardDAO, ReviewHistoryDAO
from src.domain.transaction import ITransactionContext
from src.infrastructure.database.dao.reading_item_dao import SqlAlchemyReadingItemDAO
from src.infrastructure.database.dao.review_card_dao import SqlAlchemyReviewCardDAO
from src.infrastructure.database.dao.review_history_dao import SqlAlchemyReviewHistoryDAO
from src.infrastructure.database.session import build_session_factory
from src.infrastructure.llm.openai_client import OpenAILLMClient
from src.settings.openai import OpenAISettings
from src.settings.postgres import PostgresSettings
from src.use_cases.insights.generate_weekly_summary import GenerateWeeklySummaryUseCase
from src.use_cases.reading.get_reading_stats import GetReadingStatsUseCase
from src.use_cases.reading.list_reading_items import ListReadingItemsUseCase
from src.use_cases.reading.log_reading_item import LogReadingItemUseCase
from src.use_cases.review.generate_review_question import GenerateReviewQuestionUseCase
from src.use_cases.review.get_due_reviews import GetDueReviewsUseCase
from src.use_cases.review.get_retention_stats import GetRetentionStatsUseCase
from src.use_cases.review.submit_review_grade import SubmitReviewGradeUseCase

_request_session: ContextVar[AsyncSession | None] = ContextVar("request_session", default=None)

container: punq.Container = punq.Container()
_initialized: bool = False


def get_request_session() -> AsyncSession:
    session = _request_session.get()
    if session is None:
        raise RuntimeError("Сессия БД не инициализирована для текущего запроса")
    return session


def set_request_session(session: AsyncSession) -> object:
    return _request_session.set(session)


def reset_request_session(token: object) -> None:
    _request_session.reset(token)  # type: ignore[arg-type]


def setup_container() -> None:
    global _initialized
    if _initialized:
        return

    pg = PostgresSettings()
    openai_cfg = OpenAISettings()

    session_factory = build_session_factory(dsn=pg.dsn)

    # --- синглтоны ---
    container.register(httpx.AsyncClient, instance=httpx.AsyncClient())
    container.register(async_sessionmaker, instance=session_factory)

    container.register(
        LLMClient,
        factory=lambda: OpenAILLMClient(
            http_client=container.resolve(httpx.AsyncClient),
            api_key=openai_cfg.api_key,
            model=openai_cfg.model,
            timeout_seconds=openai_cfg.timeout_seconds,
        ),
        scope=punq.Scope.singleton,
    )

    # --- транзакционный контекст (transient — новый на каждый resolve) ---
    container.register(
        ITransactionContext,
        factory=lambda: _make_transaction_context(),
        scope=punq.Scope.transient,
    )

    # --- DAO ---
    container.register(ReadingItemDAO, factory=SqlAlchemyReadingItemDAO, scope=punq.Scope.transient)
    container.register(ReviewCardDAO, factory=SqlAlchemyReviewCardDAO, scope=punq.Scope.transient)
    container.register(ReviewHistoryDAO, factory=SqlAlchemyReviewHistoryDAO, scope=punq.Scope.transient)

    # --- use cases ---
    container.register(LogReadingItemUseCase, scope=punq.Scope.transient)
    container.register(ListReadingItemsUseCase, scope=punq.Scope.transient)
    container.register(GetReadingStatsUseCase, scope=punq.Scope.transient)
    container.register(GetDueReviewsUseCase, scope=punq.Scope.transient)
    container.register(GenerateReviewQuestionUseCase, scope=punq.Scope.transient)
    container.register(SubmitReviewGradeUseCase, scope=punq.Scope.transient)
    container.register(GetRetentionStatsUseCase, scope=punq.Scope.transient)
    container.register(GenerateWeeklySummaryUseCase, scope=punq.Scope.transient)

    _initialized = True


def _make_transaction_context() -> ITransactionContext:
    from src.infrastructure.database.transaction import SqlAlchemyTransactionContext

    return SqlAlchemyTransactionContext(session_factory=container.resolve(async_sessionmaker))
