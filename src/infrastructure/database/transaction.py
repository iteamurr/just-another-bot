from __future__ import annotations

from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.infrastructure.database.session_context import reset_request_session, set_request_session
from src.domain.transaction import ITransactionContext


class SqlAlchemyTransactionContext(ITransactionContext):
    def __init__(self, *, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._factory = session_factory
        self._session: AsyncSession | None = None
        self._token: object = None

    async def __aenter__(self) -> Self:
        self._session = self._factory()
        await self._session.__aenter__()
        await self._session.begin()
        self._token = set_request_session(self._session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_traceback: TracebackType | None,
    ) -> None:
        assert self._session is not None
        if exc_type is not None:
            await self._session.rollback()
        else:
            await self._session.commit()
        await self._session.__aexit__(exc_type, exc_value, exc_traceback)
        reset_request_session(self._token)
