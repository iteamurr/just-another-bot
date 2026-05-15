from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.container import setup_container
from src.presentation.api.v1.insights.handlers import router as insights_router
from src.presentation.api.v1.reading.handlers import router as reading_router
from src.presentation.api.v1.review.handlers import router as review_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    setup_container()
    yield


app = FastAPI(title="SpacedReader", version="0.1.0", lifespan=lifespan)

_API_PREFIX = "/api/v1"

app.include_router(reading_router, prefix=_API_PREFIX)
app.include_router(review_router, prefix=_API_PREFIX)
app.include_router(insights_router, prefix=_API_PREFIX)
