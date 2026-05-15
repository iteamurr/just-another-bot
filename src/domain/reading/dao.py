from __future__ import annotations

from abc import ABC, abstractmethod

from src.domain.reading.entities import ReadingItem


class ReadingItemDAO(ABC):
    @abstractmethod
    async def save(self, item: ReadingItem) -> ReadingItem:
        pass

    @abstractmethod
    async def get_by_id(self, item_id: str) -> ReadingItem | None:
        pass

    @abstractmethod
    async def list(
        self,
        *,
        tag: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[ReadingItem]:
        pass

    @abstractmethod
    async def count(self, *, tag: str | None = None) -> int:
        pass

    @abstractmethod
    async def count_by_week(self) -> list[dict[str, int]]:
        """Количество добавлений по неделям за последние 12 недель: [{week, count}]"""
        pass

    @abstractmethod
    async def count_by_tag(self) -> list[dict[str, int]]:
        """Количество элементов по тегу: [{tag, count}]"""
        pass
