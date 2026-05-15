from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.container import get_request_session


class BaseDAO:
    @property
    def session(self) -> AsyncSession:
        return get_request_session()
