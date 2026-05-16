from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class Pagination:
    limit: int = 20
    offset: int = 0
