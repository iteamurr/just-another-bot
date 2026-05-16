"""Фикстуры интеграционных тестов — реальный Postgres через testcontainers"""

from __future__ import annotations

from types import TracebackType
from typing import Self

import punq
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer

import src.infrastructure.database.models.reading_item  # noqa: F401
import src.infrastructure.database.models.review_card  # noqa: F401
import src.infrastructure.database.models.review_history  # noqa: F401
from src.container import container
from src.infrastructure.database.session_context import reset_request_session, set_request_session
from src.domain.llm.client import LLMClient
from src.domain.transaction import ITransactionContext
from src.infrastructure.database.models.base import Base
from tests.unit.use_cases.fakes import FakeLLMClient


class _TestTransactionContext(ITransactionContext):
    """Использует готовую сессию теста; не открывает новую транзакцию"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._token: object = None

    async def __aenter__(self) -> Self:
        self._token = set_request_session(self._session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_traceback: TracebackType | None,
    ) -> None:
        reset_request_session(self._token)


@pytest.fixture(scope="session")
def postgres_container():  # type: ignore[return]
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg


@pytest.fixture(scope="session")
def db_dsn(postgres_container: PostgresContainer) -> str:
    url = postgres_container.get_connection_url()
    return url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")


@pytest.fixture(scope="session")
async def session_factory(db_dsn: str) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(db_dsn)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture(scope="session", autouse=True)
def override_llm_client() -> None:
    """Заменяем реальный LLM-клиент на фейк для всех интеграционных тестов"""
    container.register(LLMClient, instance=FakeLLMClient())


@pytest.fixture()
async def api_client(session_factory: async_sessionmaker[AsyncSession]) -> AsyncClient:
    """TestClient с реальным Postgres; откат после каждого теста через savepoint"""
    from src.main import app

    session = session_factory()
    await session.__aenter__()
    await session.begin()

    container.register(
        ITransactionContext,
        factory=lambda: _TestTransactionContext(session),
        scope=punq.Scope.transient,
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    await session.rollback()
    await session.__aexit__(None, None, None)

    from src.container import _make_transaction_context

    container.register(
        ITransactionContext,
        factory=lambda: _make_transaction_context(),
        scope=punq.Scope.transient,
    )
