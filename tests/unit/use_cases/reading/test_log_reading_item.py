"""Use case: добавление элемента чтения с созданием карточки"""

from __future__ import annotations

from datetime import UTC

import pytest

from src.domain.reading.exceptions import InvalidTakeawayLengthException
from src.use_cases.reading.log_reading_item import LogReadingItemCommand, LogReadingItemUseCase
from tests.unit.use_cases.fakes import (
    FakeDateTimeProvider,
    FakeTransactionContext,
    InMemoryReadingItemDAO,
    InMemoryReviewCardDAO,
)


@pytest.fixture()
def use_case() -> LogReadingItemUseCase:
    return LogReadingItemUseCase(
        transaction_context=FakeTransactionContext(),
        datetime_provider=FakeDateTimeProvider(),
        reading_item_dao=InMemoryReadingItemDAO(),
        review_card_dao=InMemoryReviewCardDAO(),
    )


async def test_creates_item_and_card(use_case: LogReadingItemUseCase) -> None:
    cmd = LogReadingItemCommand.new(
        title="Тестовая книга",
        source_kind="book",
        takeaway="а" * 50,
    )
    result = await use_case.execute(cmd)

    assert result.item.title == "Тестовая книга"
    assert result.card.item_id == result.item.id


async def test_card_due_immediately(use_case: LogReadingItemUseCase) -> None:
    from datetime import datetime

    cmd = LogReadingItemCommand.new(
        title="Статья",
        source_kind="article",
        takeaway="б" * 50,
    )
    result = await use_case.execute(cmd)

    assert result.card.due_at <= datetime.now(tz=UTC)


async def test_tags_stored(use_case: LogReadingItemUseCase) -> None:
    cmd = LogReadingItemCommand.new(
        title="Подкаст",
        source_kind="podcast",
        takeaway="в" * 50,
        tags=["python", "ai"],
    )
    result = await use_case.execute(cmd)
    assert result.item.tags == ["python", "ai"]


async def test_invalid_takeaway_raises(use_case: LogReadingItemUseCase) -> None:
    with pytest.raises(InvalidTakeawayLengthException):
        LogReadingItemCommand.new(
            title="Книга",
            source_kind="book",
            takeaway="коротко",
        )
