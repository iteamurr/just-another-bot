from __future__ import annotations

from fastapi import APIRouter, status

from src.domain.review.exceptions import LLMError
from src.presentation.api.dependencies import resolve_depends
from src.presentation.api.http_exceptions import DOMAIN_API_HTTP_502
from src.presentation.api.v1.insights.schemas import WeeklySummaryResponse
from src.use_cases.insights.generate_weekly_summary import GenerateWeeklySummaryUseCase

router: APIRouter = APIRouter(prefix="/insights", tags=["insights"])


@router.post(
    "/weekly",
    response_model=WeeklySummaryResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_weekly_summary(
    use_case: GenerateWeeklySummaryUseCase = resolve_depends(GenerateWeeklySummaryUseCase),
) -> WeeklySummaryResponse:
    try:
        result = await use_case.execute()
    except LLMError as exc:
        raise DOMAIN_API_HTTP_502(exc) from exc

    return WeeklySummaryResponse.from_domain(result)
