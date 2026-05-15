from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

from src.domain.review.value_objects import EaseFactor, Grade


@dataclass(slots=True, kw_only=True)
class ReviewCard:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    item_id: str
    ease_factor: EaseFactor = field(default_factory=EaseFactor.default)
    interval_days: int = 1
    repetitions: int = 0
    due_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
    cached_question: str | None = None

    def apply_grade(self, grade: Grade, now: datetime) -> None:
        """Алгоритм SM-2: обновляет ease_factor, interval_days, repetitions, due_at"""
        g = grade.value

        if g < 3:
            # провал — сброс прогресса
            self.repetitions = 0
            self.interval_days = 1
        else:
            if self.repetitions == 0:
                self.interval_days = 1
            elif self.repetitions == 1:
                self.interval_days = 6
            else:
                self.interval_days = round(self.interval_days * self.ease_factor.value)
            self.repetitions += 1

        new_ef = self.ease_factor.value + (0.1 - (5 - g) * (0.08 + (5 - g) * 0.02))
        self.ease_factor = EaseFactor(value=new_ef)
        self.due_at = now + timedelta(days=self.interval_days)
        # сбрасываем кешированный вопрос — следующий повтор генерирует новый
        self.cached_question = None


@dataclass(slots=True, kw_only=True)
class ReviewHistoryEntry:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    card_id: str
    grade: int
    ease_factor_after: float
    interval_days_after: int
    reviewed_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
