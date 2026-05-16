from __future__ import annotations

from typing import TypeVar

from fastapi import Depends, Query

from src.container import container
from src.domain.pagination import Pagination

T = TypeVar("T")


def resolve_depends(depends_type: type[T]) -> T:
    return Depends(lambda: container.resolve(depends_type))  # type: ignore[return-value]


def pagination_depends(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> Pagination:
    return Pagination(limit=limit, offset=offset)
