from __future__ import annotations

from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession

_request_session: ContextVar[AsyncSession | None] = ContextVar("request_session", default=None)


def get_request_session() -> AsyncSession:
    session = _request_session.get()
    if session is None:
        raise RuntimeError("Сессия БД не инициализирована для текущего запроса")
    return session


def set_request_session(session: AsyncSession) -> object:
    return _request_session.set(session)


def reset_request_session(token: object) -> None:
    _request_session.reset(token)  # type: ignore[arg-type]
