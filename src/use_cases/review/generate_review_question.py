from __future__ import annotations

from dataclasses import dataclass

from src.domain.llm.client import LLMClient
from src.domain.reading.dao import ReadingItemDAO
from src.domain.reading.exceptions import ReadingItemNotFoundException
from src.domain.review.dao import ReviewCardDAO
from src.domain.review.exceptions import ReviewCardNotFoundException


@dataclass(frozen=True, slots=True, kw_only=True)
class GenerateReviewQuestionCommand:
    card_id: str


@dataclass(frozen=True, slots=True, kw_only=True)
class GenerateReviewQuestionResult:
    card_id: str
    question: str


@dataclass(frozen=True, slots=True, kw_only=True)
class GenerateReviewQuestionUseCase:
    review_card_dao: ReviewCardDAO
    reading_item_dao: ReadingItemDAO
    llm_client: LLMClient

    async def execute(self, command: GenerateReviewQuestionCommand) -> GenerateReviewQuestionResult:
        card = await self.review_card_dao.get_by_id(command.card_id)
        if card is None:
            raise ReviewCardNotFoundException(card_id=command.card_id)

        # возвращаем кешированный вопрос если есть
        if card.cached_question is not None:
            return GenerateReviewQuestionResult(card_id=card.id, question=card.cached_question)

        item = await self.reading_item_dao.get_by_id(card.item_id)
        if item is None:
            raise ReadingItemNotFoundException(item_id=card.item_id)

        question = await self.llm_client.generate_review_question(takeaway=item.takeaway.text)
        card.cached_question = question
        await self.review_card_dao.save(card)

        return GenerateReviewQuestionResult(card_id=card.id, question=question)
