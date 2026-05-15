"""Интеграционные тесты роутов reading"""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.fixture()
def valid_payload() -> dict[str, object]:
    return {
        "title": "Чистый код",
        "source_kind": "book",
        "takeaway": "Функции должны делать одно дело и делать это хорошо — единственная обязанность",
        "tags": ["programming", "clean-code"],
    }


async def test_log_reading_item_created(api_client: AsyncClient, valid_payload: dict[str, object]) -> None:
    response = await api_client.post("/api/v1/reading/items", json=valid_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == valid_payload["title"]
    assert "id" in data


async def test_log_reading_item_invalid_takeaway(api_client: AsyncClient) -> None:
    response = await api_client.post(
        "/api/v1/reading/items",
        json={"title": "Книга", "source_kind": "book", "takeaway": "коротко"},
    )
    assert response.status_code == 400
    assert response.json()["detail"]["alias"] == "reading_item.invalid_takeaway_length"


async def test_list_reading_items_empty(api_client: AsyncClient) -> None:
    response = await api_client.get("/api/v1/reading/items")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


async def test_list_reading_items_returns_created(api_client: AsyncClient, valid_payload: dict[str, object]) -> None:
    await api_client.post("/api/v1/reading/items", json=valid_payload)
    response = await api_client.get("/api/v1/reading/items")
    assert response.status_code == 200
    items = response.json()["items"]
    assert any(i["title"] == valid_payload["title"] for i in items)


async def test_reading_stats_returns_structure(api_client: AsyncClient) -> None:
    response = await api_client.get("/api/v1/reading/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_items" in data
    assert "by_week" in data
    assert "by_tag" in data
