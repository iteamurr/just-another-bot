from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from src.domain.reading.value_objects import ReadingSource, Takeaway


@dataclass(slots=True, kw_only=True)
class ReadingItem:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    source: ReadingSource
    takeaway: Takeaway
    tags: list[str] = field(default_factory=list)
    finished_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
