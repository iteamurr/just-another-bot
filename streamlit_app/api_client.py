"""HTTP-клиент для обращения к FastAPI-бэкенду"""

from __future__ import annotations

import os
from typing import Any

import httpx

_BASE_URL = os.getenv("APP_BACKEND_URL", "http://localhost:8000")
_TIMEOUT = 30.0


def _client() -> httpx.Client:
    return httpx.Client(base_url=_BASE_URL, timeout=_TIMEOUT)


def log_reading_item(
    *,
    title: str,
    source_kind: str,
    source_url: str | None,
    takeaway: str,
    tags: list[str],
) -> dict[str, Any]:
    with _client() as c:
        r = c.post(
            "/api/v1/reading/items",
            json={
                "title": title,
                "source_kind": source_kind,
                "source_url": source_url,
                "takeaway": takeaway,
                "tags": tags,
            },
        )
        r.raise_for_status()
        return r.json()


def list_reading_items(
    *,
    tag: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    params: dict[str, Any] = {"limit": limit, "offset": offset}
    if tag:
        params["tag"] = tag
    with _client() as c:
        r = c.get("/api/v1/reading/items", params=params)
        r.raise_for_status()
        return r.json()


def get_reading_stats() -> dict[str, Any]:
    with _client() as c:
        r = c.get("/api/v1/reading/stats")
        r.raise_for_status()
        return r.json()


def get_due_reviews() -> dict[str, Any]:
    with _client() as c:
        r = c.get("/api/v1/reviews/due")
        r.raise_for_status()
        return r.json()


def generate_question(card_id: str) -> dict[str, Any]:
    with _client() as c:
        r = c.post(f"/api/v1/reviews/{card_id}/question")
        r.raise_for_status()
        return r.json()


def submit_grade(card_id: str, grade: int) -> dict[str, Any]:
    with _client() as c:
        r = c.post(f"/api/v1/reviews/{card_id}/grade", json={"grade": grade})
        r.raise_for_status()
        return r.json()


def get_retention_stats() -> dict[str, Any]:
    with _client() as c:
        r = c.get("/api/v1/reviews/stats")
        r.raise_for_status()
        return r.json()


def generate_weekly_summary() -> dict[str, Any]:
    with _client() as c:
        r = c.post("/api/v1/insights/weekly")
        r.raise_for_status()
        return r.json()
