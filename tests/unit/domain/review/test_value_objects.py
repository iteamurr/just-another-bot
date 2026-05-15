"""Валидация value objects"""

from __future__ import annotations

import pytest

from src.domain.reading.value_objects import Takeaway
from src.domain.review.exceptions import InvalidGradeException
from src.domain.review.value_objects import EaseFactor, Grade


class TestGrade:
    def test_valid_boundaries(self) -> None:
        for v in range(6):
            assert Grade(value=v).value == v

    def test_below_zero_raises(self) -> None:
        with pytest.raises(InvalidGradeException):
            Grade(value=-1)

    def test_above_five_raises(self) -> None:
        with pytest.raises(InvalidGradeException):
            Grade(value=6)


class TestEaseFactor:
    def test_normal_value_stored(self) -> None:
        ef = EaseFactor(value=2.5)
        assert ef.value == 2.5

    def test_below_floor_clamped(self) -> None:
        ef = EaseFactor(value=1.0)
        assert ef.value == EaseFactor.FLOOR

    def test_exact_floor_stored(self) -> None:
        ef = EaseFactor(value=1.3)
        assert ef.value == 1.3

    def test_default_is_2_5(self) -> None:
        assert EaseFactor.default().value == 2.5


class TestTakeaway:
    def test_valid_text(self) -> None:
        text = "а" * 20
        assert Takeaway(text=text).text == text

    def test_too_short_raises(self) -> None:
        from src.domain.reading.exceptions import InvalidTakeawayLengthException

        with pytest.raises(InvalidTakeawayLengthException):
            Takeaway(text="коротко")

    def test_too_long_raises(self) -> None:
        from src.domain.reading.exceptions import InvalidTakeawayLengthException

        with pytest.raises(InvalidTakeawayLengthException):
            Takeaway(text="а" * 501)

    def test_exact_min_length(self) -> None:
        Takeaway(text="а" * 20)

    def test_exact_max_length(self) -> None:
        Takeaway(text="а" * 500)
