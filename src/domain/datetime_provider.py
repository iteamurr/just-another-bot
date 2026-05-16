from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime


class IDateTimeProvider(ABC):
    @abstractmethod
    def now(self) -> datetime:
        """Возвращает текущее UTC-время"""
