from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SourceKind(StrEnum):
    ARTICLE = "article"
    BOOK = "book"
    PAPER = "paper"
    PODCAST = "podcast"
    OTHER = "other"


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadingSource:
    kind: SourceKind
    url: str | None = None


TAKEAWAY_MIN_LENGTH = 20
TAKEAWAY_MAX_LENGTH = 500


@dataclass(frozen=True, slots=True, kw_only=True)
class Takeaway:
    text: str

    def __post_init__(self) -> None:
        from src.domain.reading.exceptions import InvalidTakeawayLengthException

        length = len(self.text)
        if not (TAKEAWAY_MIN_LENGTH <= length <= TAKEAWAY_MAX_LENGTH):
            raise InvalidTakeawayLengthException(
                actual_length=length,
                min_length=TAKEAWAY_MIN_LENGTH,
                max_length=TAKEAWAY_MAX_LENGTH,
            )
