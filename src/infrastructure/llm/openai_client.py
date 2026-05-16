from __future__ import annotations

import httpx
from openai import AsyncOpenAI

from src.domain.llm.client import LLMClient
from src.domain.reading.entities import ReadingItem
from src.domain.review.exceptions import LLMResponseInvalidException, LLMUnavailableException


class OpenAILLMClient(LLMClient):
    def __init__(
        self,
        *,
        http_client: httpx.AsyncClient,
        api_key: str,
        model: str,
        timeout_seconds: float,
    ) -> None:
        self._client = AsyncOpenAI(
            api_key=api_key,
            http_client=http_client,
            timeout=timeout_seconds,
        )
        self._model = model

    async def generate_review_question(self, *, takeaway: str) -> str:
        prompt = (
            "На основе следующей заметки сгенерируй один вопрос для повторения (на русском).\n\n"
            f"Заметка: {takeaway}\n\nВопрос:"
        )
        return await self._complete(prompt)

    async def generate_weekly_summary(self, *, items: list[ReadingItem]) -> str:
        lines = "\n".join(f"- {item.title}: {item.takeaway.text}" for item in items)
        prompt = (
            "Сделай краткое резюме прочитанного за неделю (2–4 абзаца, на русском).\n\n" f"Список:\n{lines}\n\nРезюме:"
        )
        return await self._complete(prompt)

    async def _complete(self, prompt: str) -> str:
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as exc:
            raise LLMUnavailableException() from exc

        content = response.choices[0].message.content
        if not content:
            raise LLMResponseInvalidException(reason="пустой ответ от модели")
        return content.strip()
