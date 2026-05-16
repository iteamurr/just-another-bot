from __future__ import annotations

from src.domain.llm.client import LLMClient
from src.domain.reading.entities import ReadingItem


class FakeLLMClient(LLMClient):
    """Детерминированный клиент для тестов — не делает HTTP-запросов"""

    async def generate_review_question(self, *, takeaway: str) -> str:
        return f"[fake] О чём говорится в: «{takeaway[:40]}»?"

    async def generate_weekly_summary(self, *, items: list[ReadingItem]) -> str:
        titles = ", ".join(item.title for item in items)
        return f"[fake] Резюме за неделю: {titles}"
