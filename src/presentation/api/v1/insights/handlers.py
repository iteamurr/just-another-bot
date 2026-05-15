from __future__ import annotations

from fastapi import APIRouter, Depends, status

from src.domain.llm.client import LLMClient
from src.domain.reading.dao import ReadingItemDAO
from src.domain.review.exceptions import LLMError
from src.presentation.api.dependencies import get_llm_client, get_reading_item_dao
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
    reading_item_dao: ReadingItemDAO = Depends(get_reading_item_dao),
    llm_client: LLMClient = Depends(get_llm_client),
) -> WeeklySummaryResponse:
    use_case = GenerateWeeklySummaryUseCase(
        reading_item_dao=reading_item_dao,
        llm_client=llm_client,
    )

    try:
        result = await use_case.execute()
    except LLMError as exc:
        raise DOMAIN_API_HTTP_502(exc) from exc

    return WeeklySummaryResponse(summary=result.summary, items_count=result.items_count)
