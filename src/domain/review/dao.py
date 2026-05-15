from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from src.domain.review.entities import ReviewCard, ReviewHistoryEntry


@dataclass(frozen=True, slots=True, kw_only=True)
class RetentionStats:
    overall_retention: float
    avg_ease_factor: float
    total_reviews: int


class ReviewCardDAO(ABC):
    @abstractmethod
    async def save(self, card: ReviewCard) -> ReviewCard:
        """Сохраняет или обновляет карточку повторения"""

    @abstractmethod
    async def get_by_id(self, card_id: str) -> ReviewCard | None:
        """Возвращает карточку по идентификатору"""

    @abstractmethod
    async def get_by_item_id(self, item_id: str) -> ReviewCard | None:
        """Возвращает карточку по идентификатору элемента чтения"""

    @abstractmethod
    async def list_due(self, *, now: datetime, limit: int = 20) -> list[ReviewCard]:
        """Возвращает карточки с наступившей датой повторения"""

    @abstractmethod
    async def count_due(self, *, now: datetime) -> int:
        """Возвращает количество карточек с наступившей датой повторения"""

    @abstractmethod
    async def retention_stats(self) -> RetentionStats:
        """Возвращает агрегированную статистику удержания по всем повторениям"""


class ReviewHistoryDAO(ABC):
    @abstractmethod
    async def append(self, entry: ReviewHistoryEntry) -> ReviewHistoryEntry:
        """Добавляет запись в историю повторений"""

    @abstractmethod
    async def list_by_card(self, card_id: str) -> list[ReviewHistoryEntry]:
        """Возвращает историю повторений для карточки"""
