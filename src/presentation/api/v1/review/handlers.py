from __future__ import annotations

from fastapi import APIRouter, Depends, status

from src.domain.llm.client import LLMClient
from src.domain.reading.dao import ReadingItemDAO
from src.domain.reading.exceptions import ReadingItemNotFoundException
from src.domain.review.dao import ReviewCardDAO, ReviewHistoryDAO
from src.domain.review.exceptions import (
    GradeError,
    LLMError,
    ReviewCardNotFoundException,
)
from src.presentation.api.dependencies import (
    get_llm_client,
    get_reading_item_dao,
    get_review_card_dao,
    get_review_history_dao,
)
from src.presentation.api.http_exceptions import (
    DOMAIN_API_HTTP_400,
    DOMAIN_API_HTTP_404,
    DOMAIN_API_HTTP_502,
)
from src.presentation.api.v1.review.schemas import (
    DueReviewsResponse,
    RetentionStatsResponse,
    ReviewCardResponse,
    ReviewQuestionResponse,
    SubmitGradeRequest,
    SubmitGradeResponse,
)
from src.use_cases.review.generate_review_question import (
    GenerateReviewQuestionCommand,
    GenerateReviewQuestionUseCase,
)
from src.use_cases.review.get_due_reviews import GetDueReviewsUseCase
from src.use_cases.review.get_retention_stats import GetRetentionStatsUseCase
from src.use_cases.review.submit_review_grade import (
    SubmitReviewGradeCommand,
    SubmitReviewGradeUseCase,
)

router: APIRouter = APIRouter(prefix="/reviews", tags=["reviews"])


def _to_card_response(card: object) -> ReviewCardResponse:
    from src.domain.review.entities import ReviewCard

    assert isinstance(card, ReviewCard)
    return ReviewCardResponse(
        id=card.id,
        item_id=card.item_id,
        ease_factor=card.ease_factor.value,
        interval_days=card.interval_days,
        repetitions=card.repetitions,
        due_at=card.due_at,
        cached_question=card.cached_question,
    )


@router.get("/due", response_model=DueReviewsResponse)
async def get_due_reviews(
    review_card_dao: ReviewCardDAO = Depends(get_review_card_dao),
) -> DueReviewsResponse:
    use_case = GetDueReviewsUseCase(review_card_dao=review_card_dao)
    result = await use_case.execute()
    return DueReviewsResponse(
        cards=[_to_card_response(c) for c in result.cards],
        total_due=result.total_due,
    )


@router.post(
    "/{card_id}/question",
    response_model=ReviewQuestionResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_review_question(
    card_id: str,
    review_card_dao: ReviewCardDAO = Depends(get_review_card_dao),
    reading_item_dao: ReadingItemDAO = Depends(get_reading_item_dao),
    llm_client: LLMClient = Depends(get_llm_client),
) -> ReviewQuestionResponse:
    use_case = GenerateReviewQuestionUseCase(
        review_card_dao=review_card_dao,
        reading_item_dao=reading_item_dao,
        llm_client=llm_client,
    )
    command = GenerateReviewQuestionCommand(card_id=card_id)

    try:
        result = await use_case.execute(command)
    except ReviewCardNotFoundException as exc:
        raise DOMAIN_API_HTTP_404(exc) from exc
    except ReadingItemNotFoundException as exc:
        raise DOMAIN_API_HTTP_404(exc) from exc
    except LLMError as exc:
        raise DOMAIN_API_HTTP_502(exc) from exc

    return ReviewQuestionResponse(card_id=result.card_id, question=result.question)


@router.post(
    "/{card_id}/grade",
    response_model=SubmitGradeResponse,
    status_code=status.HTTP_200_OK,
)
async def submit_review_grade(
    card_id: str,
    request: SubmitGradeRequest,
    review_card_dao: ReviewCardDAO = Depends(get_review_card_dao),
    review_history_dao: ReviewHistoryDAO = Depends(get_review_history_dao),
) -> SubmitGradeResponse:
    use_case = SubmitReviewGradeUseCase(
        review_card_dao=review_card_dao,
        review_history_dao=review_history_dao,
    )

    try:
        command = SubmitReviewGradeCommand.new(card_id=card_id, grade=request.grade)
        result = await use_case.execute(command)
    except ReviewCardNotFoundException as exc:
        raise DOMAIN_API_HTTP_404(exc) from exc
    except GradeError as exc:
        raise DOMAIN_API_HTTP_400(exc) from exc

    card = result.card
    return SubmitGradeResponse(
        card_id=card.id,
        new_interval_days=card.interval_days,
        new_ease_factor=card.ease_factor.value,
        due_at=card.due_at,
    )


@router.get("/stats", response_model=RetentionStatsResponse)
async def get_retention_stats(
    review_card_dao: ReviewCardDAO = Depends(get_review_card_dao),
) -> RetentionStatsResponse:
    use_case = GetRetentionStatsUseCase(review_card_dao=review_card_dao)
    result = await use_case.execute()
    return RetentionStatsResponse(
        overall_retention=result.overall_retention,
        avg_ease_factor=result.avg_ease_factor,
        total_reviews=result.total_reviews,
    )
