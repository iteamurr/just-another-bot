from __future__ import annotations

from pydantic import BaseModel


class WeeklySummaryResponse(BaseModel):
    summary: str
    items_count: int
