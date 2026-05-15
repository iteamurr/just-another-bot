from __future__ import annotations

from abc import ABC, abstractmethod

from src.domain.reading.entities import ReadingItem


class ReadingItemDAO(ABC):
    @abstractmethod
    async def save(self, item: ReadingItem) -> ReadingItem:
        """Сохраняет или обновляет элемент чтения"""

    @abstractmethod
    async def get_by_id(self, item_id: str) -> ReadingItem | None:
        """Возвращает элемент чтения по идентификатору"""

    @abstractmethod
    async def list(
        self,
        *,
        tag: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[ReadingItem]:
        """Возвращает список элементов с фильтрацией по тегу и пагинацией"""

    @abstractmethod
    async def count(self, *, tag: str | None = None) -> int:
        """Возвращает количество элементов, опционально по тегу"""

    @abstractmethod
    async def count_by_week(self) -> list[dict[str, int]]:
        """Возвращает количество добавлений по неделям за последние 12 недель"""

    @abstractmethod
    async def count_by_tag(self) -> list[dict[str, int]]:
        """Возвращает количество элементов сгруппированное по тегу"""
