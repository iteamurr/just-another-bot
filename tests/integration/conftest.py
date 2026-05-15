"""Фикстуры интеграционных тестов — реальный Postgres через testcontainers"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer

import src.infrastructure.database.models.reading_item  # noqa: F401
import src.infrastructure.database.models.review_card  # noqa: F401
import src.infrastructure.database.models.review_history  # noqa: F401
from src.infrastructure.database.models.base import Base


@pytest.fixture(scope="session")
def postgres_container():  # type: ignore[return]
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg


@pytest.fixture(scope="session")
def db_dsn(postgres_container: PostgresContainer) -> str:
    url = postgres_container.get_connection_url()
    # testcontainers возвращает psycopg2 URL — меняем драйвер
    return url.replace("postgresql+psycopg2://", "postgresql+asyncpg://")


@pytest.fixture(scope="session")
async def session_factory(db_dsn: str) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(db_dsn)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    return factory


@pytest.fixture()
async def db_session(session_factory: async_sessionmaker[AsyncSession]) -> AsyncSession:
    async with session_factory() as session:
        async with session.begin():
            yield session
            await session.rollback()  # откат после каждого теста


@pytest.fixture()
async def api_client(session_factory: async_sessionmaker[AsyncSession]) -> AsyncClient:
    """TestClient с реальным Postgres — сессия подменяется через override"""
    from src.main import app
    from src.presentation.api.dependencies import get_db_session

    async def _override_session():  # type: ignore[return]
        async with session_factory() as session:
            async with session.begin():
                yield session
                await session.rollback()

    app.dependency_overrides[get_db_session] = _override_session

    # подменяем LLMClient на фейк
    from src.presentation.api.dependencies import get_llm_client
    from tests.unit.use_cases.fakes import FakeLLMClient

    fake_llm = FakeLLMClient()
    app.dependency_overrides[get_llm_client] = lambda: fake_llm

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
