from __future__ import annotations

from typing import TypeVar

from fastapi import Depends

from src.container import container

T = TypeVar("T")


def resolve_depends(depends_type: type[T]) -> T:
    return Depends(lambda: container.resolve(depends_type))  # type: ignore[return-value]
