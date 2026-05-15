from __future__ import annotations

from fastapi import APIRouter, status

from src.domain.reading.exceptions import ReadingItemNotFoundException
from src.domain.review.exceptions import GradeError, LLMError, ReviewCardNotFoundException
from src.presentation.api.dependencies import resolve_depends
from src.presentation.api.http_exceptions import DOMAIN_API_HTTP_400, DOMAIN_API_HTTP_404, DOMAIN_API_HTTP_502
from src.presentation.api.v1.review.schemas import (
    DueReviewsResponse,
    RetentionStatsResponse,
    ReviewQuestionResponse,
    SubmitGradeRequest,
    SubmitGradeResponse,
)
from src.use_cases.review.generate_review_question import GenerateReviewQuestionCommand, GenerateReviewQuestionUseCase
from src.use_cases.review.get_due_reviews import GetDueReviewsUseCase
from src.use_cases.review.get_retention_stats import GetRetentionStatsUseCase
from src.use_cases.review.submit_review_grade import SubmitReviewGradeCommand, SubmitReviewGradeUseCase

router: APIRouter = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get(
    "/due",
    response_model=DueReviewsResponse,
)
async def get_due_reviews(
    use_case: GetDueReviewsUseCase = resolve_depends(GetDueReviewsUseCase),
) -> DueReviewsResponse:
    result = await use_case.execute()
    return DueReviewsResponse.from_domain(result)


@router.post(
    "/{card_id}/question",
    response_model=ReviewQuestionResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_review_question(
    card_id: str,
    use_case: GenerateReviewQuestionUseCase = resolve_depends(GenerateReviewQuestionUseCase),
) -> ReviewQuestionResponse:
    command = GenerateReviewQuestionCommand(card_id=card_id)
    try:
        result = await use_case.execute(command)
    except ReviewCardNotFoundException as exc:
        raise DOMAIN_API_HTTP_404(exc) from exc
    except ReadingItemNotFoundException as exc:
        raise DOMAIN_API_HTTP_404(exc) from exc
    except LLMError as exc:
        raise DOMAIN_API_HTTP_502(exc) from exc

    return ReviewQuestionResponse.from_domain(result)


@router.post(
    "/{card_id}/grade",
    response_model=SubmitGradeResponse,
    status_code=status.HTTP_200_OK,
)
async def submit_review_grade(
    card_id: str,
    request: SubmitGradeRequest,
    use_case: SubmitReviewGradeUseCase = resolve_depends(SubmitReviewGradeUseCase),
) -> SubmitGradeResponse:
    try:
        command = SubmitReviewGradeCommand.new(card_id=card_id, grade=request.grade)
        result = await use_case.execute(command)
    except ReviewCardNotFoundException as exc:
        raise DOMAIN_API_HTTP_404(exc) from exc
    except GradeError as exc:
        raise DOMAIN_API_HTTP_400(exc) from exc

    return SubmitGradeResponse.from_domain(result.card)


@router.get(
    "/stats",
    response_model=RetentionStatsResponse,
)
async def get_retention_stats(
    use_case: GetRetentionStatsUseCase = resolve_depends(GetRetentionStatsUseCase),
) -> RetentionStatsResponse:
    result = await use_case.execute()
    return RetentionStatsResponse.from_domain(result)
