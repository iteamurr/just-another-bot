"""SM-2: все ветки алгоритма"""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.domain.review.entities import ReviewCard
from src.domain.review.value_objects import EaseFactor, Grade


def _now() -> datetime:
    return datetime(2026, 1, 1, tzinfo=timezone.utc)


def _card(**kwargs: object) -> ReviewCard:
    return ReviewCard(item_id="item-1", **kwargs)  # type: ignore[arg-type]


class TestApplyGradeFailedRecall:
    """Оценка < 3 — сброс прогресса"""

    def test_resets_repetitions(self) -> None:
        card = _card(repetitions=5, interval_days=21)
        card.apply_grade(Grade(value=2), _now())
        assert card.repetitions == 0

    def test_resets_interval_to_one(self) -> None:
        card = _card(repetitions=3, interval_days=10)
        card.apply_grade(Grade(value=0), _now())
        assert card.interval_days == 1

    def test_clears_cached_question(self) -> None:
        card = _card(cached_question="вопрос?")
        card.apply_grade(Grade(value=1), _now())
        assert card.cached_question is None

    def test_ease_factor_decreases(self) -> None:
        card = _card(ease_factor=EaseFactor(value=2.5))
        before = card.ease_factor.value
        card.apply_grade(Grade(value=2), _now())
        assert card.ease_factor.value < before


class TestApplyGradeFirstRepetition:
    """repetitions == 0, оценка >= 3 → interval = 1"""

    def test_interval_is_one(self) -> None:
        card = _card(repetitions=0)
        card.apply_grade(Grade(value=5), _now())
        assert card.interval_days == 1
        assert card.repetitions == 1


class TestApplyGradeSecondRepetition:
    """repetitions == 1, оценка >= 3 → interval = 6"""

    def test_interval_is_six(self) -> None:
        card = _card(repetitions=1, interval_days=1)
        card.apply_grade(Grade(value=4), _now())
        assert card.interval_days == 6
        assert card.repetitions == 2


class TestApplyGradeNthRepetition:
    """repetitions >= 2, оценка >= 3 → interval *= ease_factor"""

    def test_interval_multiplied(self) -> None:
        card = _card(repetitions=2, interval_days=6, ease_factor=EaseFactor(value=2.5))
        card.apply_grade(Grade(value=5), _now())
        assert card.interval_days == round(6 * 2.5)

    def test_repetitions_incremented(self) -> None:
        card = _card(repetitions=4, interval_days=21)
        card.apply_grade(Grade(value=3), _now())
        assert card.repetitions == 5


class TestEaseFactorFloor:
    """EF не опускается ниже 1.3 после серии плохих оценок"""

    def test_floor_enforced(self) -> None:
        card = _card(ease_factor=EaseFactor(value=1.4))
        # оценка 2 снизит EF, но он не должен упасть ниже 1.3
        card.apply_grade(Grade(value=2), _now())
        assert card.ease_factor.value >= 1.3

    def test_perfect_grade_increases_ef(self) -> None:
        card = _card(ease_factor=EaseFactor(value=2.5), repetitions=2, interval_days=6)
        before = card.ease_factor.value
        card.apply_grade(Grade(value=5), _now())
        assert card.ease_factor.value > before


class TestDueAt:
    """due_at смещается на interval_days от now"""

    def test_due_at_shifted(self) -> None:
        from datetime import timedelta

        now = _now()
        card = _card(repetitions=1, interval_days=1)
        card.apply_grade(Grade(value=5), now)
        expected = now + timedelta(days=card.interval_days)
        assert card.due_at == expected
