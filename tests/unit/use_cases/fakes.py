"""In-memory реализации DAO и LLMClient для юнит-тестов"""

from __future__ import annotations

from datetime import UTC, datetime

from src.domain.datetime_provider import IDateTimeProvider
from src.domain.llm.client import LLMClient
from src.domain.pagination import Pagination
from src.domain.reading.dao import ReadingItemDAO
from src.domain.reading.entities import ReadingItem
from src.domain.review.dao import RetentionStats, ReviewCardDAO, ReviewHistoryDAO
from src.domain.review.entities import ReviewCard, ReviewHistoryEntry
from src.domain.transaction import ITransactionContext


class InMemoryReadingItemDAO(ReadingItemDAO):
    def __init__(self) -> None:
        self._store: dict[str, ReadingItem] = {}

    async def save(self, item: ReadingItem) -> ReadingItem:
        self._store[item.id] = item
        return item

    async def get_by_id(self, item_id: str) -> ReadingItem | None:
        return self._store.get(item_id)

    async def list(
        self,
        *,
        tag: str | None = None,
        pagination: Pagination = Pagination(),
    ) -> list[ReadingItem]:
        items = list(self._store.values())
        if tag is not None:
            items = [i for i in items if tag in i.tags]
        return items[pagination.offset : pagination.offset + pagination.limit]

    async def count(self, *, tag: str | None = None) -> int:
        if tag is None:
            return len(self._store)
        return sum(1 for i in self._store.values() if tag in i.tags)

    async def count_by_week(self) -> list[dict[str, int]]:
        return []

    async def count_by_tag(self) -> list[dict[str, int]]:
        return []


class InMemoryReviewCardDAO(ReviewCardDAO):
    def __init__(self) -> None:
        self._store: dict[str, ReviewCard] = {}

    async def save(self, card: ReviewCard) -> ReviewCard:
        self._store[card.id] = card
        return card

    async def get_by_id(self, card_id: str) -> ReviewCard | None:
        return self._store.get(card_id)

    async def get_by_item_id(self, item_id: str) -> ReviewCard | None:
        return next((c for c in self._store.values() if c.item_id == item_id), None)

    async def list_due(self, *, now: datetime, limit: int = 20) -> list[ReviewCard]:
        due = [c for c in self._store.values() if c.due_at <= now]
        return sorted(due, key=lambda c: c.due_at)[:limit]

    async def count_due(self, *, now: datetime) -> int:
        return sum(1 for c in self._store.values() if c.due_at <= now)

    async def retention_stats(self) -> RetentionStats:
        return RetentionStats(overall_retention=0.0, avg_ease_factor=2.5, total_reviews=0)


class InMemoryReviewHistoryDAO(ReviewHistoryDAO):
    def __init__(self) -> None:
        self._entries: list[ReviewHistoryEntry] = []

    async def append(self, entry: ReviewHistoryEntry) -> ReviewHistoryEntry:
        self._entries.append(entry)
        return entry

    async def list_by_card(self, card_id: str) -> list[ReviewHistoryEntry]:
        return [e for e in self._entries if e.card_id == card_id]


class FakeTransactionContext(ITransactionContext):
    async def __aenter__(self) -> FakeTransactionContext:
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, exc_traceback: object
    ) -> None:
        pass


class FakeDateTimeProvider(IDateTimeProvider):
    def __init__(self, fixed: datetime | None = None) -> None:
        self._now = fixed or datetime.now(tz=UTC)

    def now(self) -> datetime:
        return self._now


class FakeLLMClient(LLMClient):
    """Детерминированный клиент для тестов"""

    async def generate_review_question(self, *, takeaway: str) -> str:
        return f"[fake] Вопрос по: «{takeaway[:40]}»"

    async def generate_weekly_summary(self, *, items: list[ReadingItem]) -> str:
        return f"[fake] Резюме: {len(items)} элементов"
