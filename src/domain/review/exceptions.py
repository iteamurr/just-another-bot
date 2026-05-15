from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.domain.exceptions import DomainException


class ReviewCardError(DomainException):
    """Абстрактная категория ошибок карточки повторения"""


class GradeError(DomainException):
    """Абстрактная категория ошибок оценки"""


class LLMError(DomainException):
    """Абстрактная категория ошибок LLM"""


@dataclass
class ReviewCardNotFoundException(ReviewCardError):
    alias = "review_card.not_found"
    description_template = "Карточка повторения {card_id} не найдена"
    card_id: str


@dataclass
class ReviewNotDueYetException(ReviewCardError):
    alias = "review_card.not_due_yet"
    description_template = "Карточка {card_id} не готова к повторению до {due_at}"
    card_id: str
    due_at: datetime


@dataclass
class InvalidGradeException(GradeError):
    alias = "grade.invalid"
    description_template = "Оценка {value} недопустима — допустимо 0..5"
    value: int


@dataclass
class LLMUnavailableException(LLMError):
    alias = "llm.unavailable"
    description_template = "LLM-сервис недоступен"


@dataclass
class LLMResponseInvalidException(LLMError):
    alias = "llm.response_invalid"
    description_template = "LLM вернул некорректный ответ: {reason}"
    reason: str
