"""Интеграционные тесты роутов insights"""

from __future__ import annotations

from httpx import AsyncClient


async def test_weekly_summary_no_items(api_client: AsyncClient) -> None:
    response = await api_client.post("/api/v1/insights/weekly")
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert data["items_count"] == 0


async def test_weekly_summary_with_items(api_client: AsyncClient) -> None:
    await api_client.post(
        "/api/v1/reading/items",
        json={
            "title": "Sapiens",
            "source_kind": "book",
            "takeaway": "История человечества — это история когнитивных революций и случайных событий",
        },
    )
    response = await api_client.post("/api/v1/insights/weekly")
    assert response.status_code == 200
    data = response.json()
    assert data["items_count"] >= 1
    assert len(data["summary"]) > 0
