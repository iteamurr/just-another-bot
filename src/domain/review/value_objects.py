from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class Grade:
    value: int

    def __post_init__(self) -> None:
        from src.domain.review.exceptions import InvalidGradeException

        if not (0 <= self.value <= 5):
            raise InvalidGradeException(value=self.value)


@dataclass(frozen=True, slots=True, kw_only=True)
class EaseFactor:
    value: float

    FLOOR: ClassVar[float] = 1.3

    def __post_init__(self) -> None:
        # SM-2: EF не опускается ниже 1.3
        if self.value < self.FLOOR:
            object.__setattr__(self, "value", self.FLOOR)

    @classmethod
    def default(cls) -> EaseFactor:
        return cls(value=2.5)
