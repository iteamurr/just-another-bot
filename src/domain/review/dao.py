from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from src.domain.review.entities import ReviewCard, ReviewHistoryEntry


class ReviewCardDAO(ABC):
    @abstractmethod
    async def save(self, card: ReviewCard) -> ReviewCard:
        pass

    @abstractmethod
    async def get_by_id(self, card_id: str) -> ReviewCard | None:
        pass

    @abstractmethod
    async def get_by_item_id(self, item_id: str) -> ReviewCard | None:
        pass

    @abstractmethod
    async def list_due(self, *, now: datetime, limit: int = 20) -> list[ReviewCard]:
        pass

    @abstractmethod
    async def count_due(self, *, now: datetime) -> int:
        pass

    @abstractmethod
    async def retention_stats(self) -> dict[str, float]:
        """Возвращает {overall_retention, avg_ease_factor, total_reviews}"""
        pass


class ReviewHistoryDAO(ABC):
    @abstractmethod
    async def append(self, entry: ReviewHistoryEntry) -> ReviewHistoryEntry:
        pass

    @abstractmethod
    async def list_by_card(self, card_id: str) -> list[ReviewHistoryEntry]:
        pass
