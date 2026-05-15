from __future__ import annotations

import punq
import httpx
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.llm.client import LLMClient
from src.infrastructure.database.session import build_session_factory
from src.infrastructure.llm.openai_client import OpenAILLMClient
from src.settings.openai import OpenAISettings
from src.settings.postgres import PostgresSettings

container: punq.Container = punq.Container()
_initialized: bool = False


def setup_container() -> None:
    global _initialized
    if _initialized:
        return

    pg = PostgresSettings()
    openai_cfg = OpenAISettings()

    # --- синглтоны ---
    http_client = httpx.AsyncClient()
    container.register(httpx.AsyncClient, instance=http_client)

    session_factory = build_session_factory(dsn=pg.dsn)
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

    _initialized = True
