"""Интеграционные тесты роутов review"""

from __future__ import annotations

from httpx import AsyncClient


async def _create_item(client: AsyncClient) -> str:
    """Вспомогательная функция — создаёт элемент и возвращает его id"""
    resp = await client.post(
        "/api/v1/reading/items",
        json={
            "title": "Мышление быстрое и медленное",
            "source_kind": "book",
            "takeaway": "Система 1 работает автоматически, система 2 — осознанно и требует усилий",
        },
    )
    assert resp.status_code == 201
    return resp.json()["id"]


async def _get_due_card_id(client: AsyncClient) -> str | None:
    resp = await client.get("/api/v1/reviews/due")
    assert resp.status_code == 200
    cards = resp.json()["cards"]
    return cards[0]["id"] if cards else None


async def test_due_reviews_after_create(api_client: AsyncClient) -> None:
    await _create_item(api_client)
    response = await api_client.get("/api/v1/reviews/due")
    assert response.status_code == 200
    data = response.json()
    assert data["total_due"] >= 1


async def test_generate_question(api_client: AsyncClient) -> None:
    await _create_item(api_client)
    card_id = await _get_due_card_id(api_client)
    assert card_id is not None

    response = await api_client.post(f"/api/v1/reviews/{card_id}/question")
    assert response.status_code == 200
    data = response.json()
    assert data["card_id"] == card_id
    assert len(data["question"]) > 0


async def test_generate_question_not_found(api_client: AsyncClient) -> None:
    response = await api_client.post("/api/v1/reviews/nonexistent-id/question")
    assert response.status_code == 404


async def test_submit_grade(api_client: AsyncClient) -> None:
    await _create_item(api_client)
    card_id = await _get_due_card_id(api_client)
    assert card_id is not None

    response = await api_client.post(f"/api/v1/reviews/{card_id}/grade", json={"grade": 4})
    assert response.status_code == 200
    data = response.json()
    assert data["card_id"] == card_id
    assert data["new_interval_days"] >= 1


async def test_submit_invalid_grade(api_client: AsyncClient) -> None:
    await _create_item(api_client)
    card_id = await _get_due_card_id(api_client)
    assert card_id is not None

    # FastAPI валидирует ge=0 le=5 на уровне схемы — 422
    response = await api_client.post(f"/api/v1/reviews/{card_id}/grade", json={"grade": 10})
    assert response.status_code == 422


async def test_retention_stats_structure(api_client: AsyncClient) -> None:
    response = await api_client.get("/api/v1/reviews/stats")
    assert response.status_code == 200
    data = response.json()
    assert "overall_retention" in data
    assert "total_reviews" in data
