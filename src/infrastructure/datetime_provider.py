from __future__ import annotations

from datetime import UTC, datetime

from src.domain.datetime_provider import IDateTimeProvider


class UtcDateTimeProvider(IDateTimeProvider):
    def now(self) -> datetime:
        return datetime.now(tz=UTC)
