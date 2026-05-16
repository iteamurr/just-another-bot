"""Use case: сабмит оценки и запись в историю"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from src.domain.review.entities import ReviewCard
from src.domain.review.exceptions import InvalidGradeException, ReviewCardNotFoundException
from src.use_cases.review.submit_review_grade import SubmitReviewGradeCommand, SubmitReviewGradeUseCase
from tests.unit.use_cases.fakes import (
    FakeDateTimeProvider,
    FakeTransactionContext,
    InMemoryReviewCardDAO,
    InMemoryReviewHistoryDAO,
)


def _make_use_case(
    card: ReviewCard | None = None,
) -> tuple[SubmitReviewGradeUseCase, InMemoryReviewCardDAO, InMemoryReviewHistoryDAO]:
    card_dao = InMemoryReviewCardDAO()
    history_dao = InMemoryReviewHistoryDAO()
    if card is not None:
        card_dao._store[card.id] = card
    use_case = SubmitReviewGradeUseCase(
        transaction_context=FakeTransactionContext(),
        datetime_provider=FakeDateTimeProvider(),
        review_card_dao=card_dao,
        review_history_dao=history_dao,
    )
    return use_case, card_dao, history_dao


async def test_grade_updates_card() -> None:
    card = ReviewCard(item_id="item-1", due_at=datetime(2020, 1, 1, tzinfo=UTC))
    use_case, card_dao, _ = _make_use_case(card)

    cmd = SubmitReviewGradeCommand.new(card_id=card.id, grade=5)
    result = await use_case.execute(cmd)

    assert result.card.repetitions == 1
    assert result.card.due_at > datetime.now(tz=UTC)


async def test_history_entry_appended() -> None:
    card = ReviewCard(item_id="item-1", due_at=datetime(2020, 1, 1, tzinfo=UTC))
    use_case, _, history_dao = _make_use_case(card)

    cmd = SubmitReviewGradeCommand.new(card_id=card.id, grade=4)
    await use_case.execute(cmd)

    entries = await history_dao.list_by_card(card.id)
    assert len(entries) == 1
    assert entries[0].grade == 4


async def test_card_not_found_raises() -> None:
    use_case, _, _ = _make_use_case()
    cmd = SubmitReviewGradeCommand.new(card_id="nonexistent", grade=3)

    with pytest.raises(ReviewCardNotFoundException):
        await use_case.execute(cmd)


async def test_invalid_grade_raises_at_command_boundary() -> None:
    with pytest.raises(InvalidGradeException):
        SubmitReviewGradeCommand.new(card_id="any", grade=6)


async def test_failed_grade_resets_interval() -> None:
    from src.domain.review.value_objects import EaseFactor

    card = ReviewCard(
        item_id="item-1",
        due_at=datetime(2020, 1, 1, tzinfo=UTC),
        repetitions=5,
        interval_days=30,
        ease_factor=EaseFactor(value=2.5),
    )
    use_case, _, _ = _make_use_case(card)

    cmd = SubmitReviewGradeCommand.new(card_id=card.id, grade=1)
    result = await use_case.execute(cmd)

    assert result.card.repetitions == 0
    assert result.card.interval_days == 1
