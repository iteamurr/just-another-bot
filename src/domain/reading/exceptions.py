from __future__ import annotations

from dataclasses import dataclass

from src.domain.exceptions import DomainException


class ReadingItemError(DomainException):
    """Абстрактная категория ошибок элемента чтения"""


class TagError(DomainException):
    """Абстрактная категория ошибок тегов"""


@dataclass
class ReadingItemNotFoundException(ReadingItemError):
    alias = "reading_item.not_found"
    description_template = "Элемент чтения {item_id} не найден"
    item_id: str


@dataclass
class InvalidTakeawayLengthException(ReadingItemError):
    alias = "reading_item.invalid_takeaway_length"
    description_template = (
        "Длина заметки {actual_length} вне допустимого диапазона [{min_length}, {max_length}]"
    )
    actual_length: int
    min_length: int
    max_length: int


@dataclass
class InvalidTagException(TagError):
    alias = "tag.invalid"
    description_template = "Тег '{tag}' недопустим"
    tag: str
