from __future__ import annotations

from pydantic import BaseModel

from src.use_cases.insights.generate_weekly_summary import GenerateWeeklySummaryResult


class WeeklySummaryResponse(BaseModel):
    summary: str
    items_count: int

    @classmethod
    def from_domain(cls, result: GenerateWeeklySummaryResult) -> WeeklySummaryResponse:
        return cls(summary=result.summary, items_count=result.items_count)
