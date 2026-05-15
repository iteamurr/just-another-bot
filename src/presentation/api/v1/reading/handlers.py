from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status

from src.domain.reading.dao import ReadingItemDAO
from src.domain.reading.exceptions import (
    InvalidTakeawayLengthException,
    ReadingItemError,
)
from src.domain.review.dao import ReviewCardDAO
from src.presentation.api.dependencies import get_reading_item_dao, get_review_card_dao
from src.presentation.api.http_exceptions import DOMAIN_API_HTTP_400, DOMAIN_API_HTTP_404
from src.presentation.api.v1.reading.schemas import (
    ListReadingItemsResponse,
    LogReadingItemRequest,
    ReadingItemResponse,
    ReadingSourceSchema,
    ReadingStatsResponse,
    TagCountSchema,
    WeekCountSchema,
)
from src.use_cases.reading.get_reading_stats import GetReadingStatsUseCase
from src.use_cases.reading.list_reading_items import ListReadingItemsQuery, ListReadingItemsUseCase
from src.use_cases.reading.log_reading_item import LogReadingItemCommand, LogReadingItemUseCase

router: APIRouter = APIRouter(prefix="/reading", tags=["reading"])


def _to_item_response(item: object) -> ReadingItemResponse:
    from src.domain.reading.entities import ReadingItem

    assert isinstance(item, ReadingItem)
    return ReadingItemResponse(
        id=item.id,
        title=item.title,
        source=ReadingSourceSchema(kind=item.source.kind.value, url=item.source.url),
        takeaway=item.takeaway.text,
        tags=item.tags,
        finished_at=item.finished_at,
        created_at=item.created_at,
    )


@router.post("/items", response_model=ReadingItemResponse, status_code=status.HTTP_201_CREATED)
async def log_reading_item(
    request: LogReadingItemRequest,
    reading_dao: ReadingItemDAO = Depends(get_reading_item_dao),
    review_dao: ReviewCardDAO = Depends(get_review_card_dao),
) -> ReadingItemResponse:
    use_case = LogReadingItemUseCase(
        reading_item_dao=reading_dao,
        review_card_dao=review_dao,
    )
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

    return _to_item_response(result.item)


@router.get("/items", response_model=ListReadingItemsResponse)
async def list_reading_items(
    tag: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    reading_dao: ReadingItemDAO = Depends(get_reading_item_dao),
) -> ListReadingItemsResponse:
    use_case = ListReadingItemsUseCase(reading_item_dao=reading_dao)
    query = ListReadingItemsQuery.new(tag=tag, limit=limit, offset=offset)

    try:
        result = await use_case.execute(query)
    except ReadingItemError as exc:
        raise DOMAIN_API_HTTP_400(exc) from exc

    return ListReadingItemsResponse(
        items=[_to_item_response(i) for i in result.items],
        total=result.total,
        limit=limit,
        offset=offset,
    )


@router.get("/stats", response_model=ReadingStatsResponse)
async def get_reading_stats(
    reading_dao: ReadingItemDAO = Depends(get_reading_item_dao),
) -> ReadingStatsResponse:
    use_case = GetReadingStatsUseCase(reading_item_dao=reading_dao)
    result = await use_case.execute()

    return ReadingStatsResponse(
        total_items=result.total_items,
        by_week=[WeekCountSchema(**row) for row in result.by_week],
        by_tag=[TagCountSchema(**row) for row in result.by_tag],
    )
