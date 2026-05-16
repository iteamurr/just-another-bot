from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status

from src.domain.pagination import Pagination
from src.domain.reading.exceptions import InvalidTakeawayLengthException, ReadingItemError
from src.presentation.api.dependencies import pagination_depends, resolve_depends
from src.presentation.api.http_exceptions import DOMAIN_API_HTTP_400
from src.presentation.api.v1.reading.schemas import (
    ListReadingItemsResponse,
    LogReadingItemRequest,
    ReadingItemResponse,
    ReadingStatsResponse,
)
from src.use_cases.reading.get_reading_stats import GetReadingStatsUseCase
from src.use_cases.reading.list_reading_items import ListReadingItemsQuery, ListReadingItemsUseCase
from src.use_cases.reading.log_reading_item import LogReadingItemCommand, LogReadingItemUseCase

router: APIRouter = APIRouter(prefix="/reading", tags=["reading"])


@router.post(
    "/items",
    response_model=ReadingItemResponse,
    status_code=status.HTTP_201_CREATED,
)
async def log_reading_item(
    request: LogReadingItemRequest,
    use_case: LogReadingItemUseCase = resolve_depends(LogReadingItemUseCase),
) -> ReadingItemResponse:
    try:
        command = LogReadingItemCommand.new(
            title=request.title,
            source_kind=request.source_kind,
            source_url=request.source_url,
            takeaway=request.takeaway,
            tags=request.tags,
            finished_at=request.finished_at,
        )
        result = await use_case.execute(command)
    except InvalidTakeawayLengthException as exc:
        raise DOMAIN_API_HTTP_400(exc) from exc
    except ReadingItemError as exc:
        raise DOMAIN_API_HTTP_400(exc) from exc

    return ReadingItemResponse.from_domain(result.item)


@router.get(
    "/items",
    response_model=ListReadingItemsResponse,
)
async def list_reading_items(
    pagination: Pagination = Depends(pagination_depends),
    tag: str | None = Query(default=None),
    use_case: ListReadingItemsUseCase = resolve_depends(ListReadingItemsUseCase),
) -> ListReadingItemsResponse:
    query = ListReadingItemsQuery.new(tag=tag, pagination=pagination)

    try:
        result = await use_case.execute(query)
    except ReadingItemError as exc:
        raise DOMAIN_API_HTTP_400(exc) from exc

    return ListReadingItemsResponse.from_domain(result, pagination=pagination)


@router.get(
    "/stats",
    response_model=ReadingStatsResponse,
)
async def get_reading_stats(
    use_case: GetReadingStatsUseCase = resolve_depends(GetReadingStatsUseCase),
) -> ReadingStatsResponse:
    result = await use_case.execute()
    return ReadingStatsResponse.from_domain(result)
