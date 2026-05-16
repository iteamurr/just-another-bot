from __future__ import annotations

from abc import ABC, abstractmethod

from src.domain.reading.entities import ReadingItem


class LLMClient(ABC):
    @abstractmethod
    async def generate_review_question(self, *, takeaway: str) -> str:
        pass

    @abstractmethod
    async def generate_weekly_summary(self, *, items: list[ReadingItem]) -> str:
        pass
