from fastapi.testclient import TestClient


def login_as_demo(client: TestClient, nickname="demo", password="demo"):
    response = client.post("/api/auth/login", json={"nickname": nickname, "password": password})
    assert response.status_code == 200, response.text


def test_get_books_returns_paginated_payload(client: TestClient):
    response = client.get("/api/books?limit=5&offset=0")
    assert response.status_code == 200
    payload = response.json()
    assert "items" in payload and isinstance(payload["items"], list)
    assert payload["limit"] == 5


def test_get_recommendations_requires_valid_param(client: TestClient):
    response = client.get("/api/recommendations?m=5")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    assert len(payload["items"]) <= payload["limit"]
    assert payload["items"][0]["ratings"] >= 0

    bad = client.get("/api/recommendations?m=0")
    assert bad.status_code == 422


def test_create_rating_requires_auth_and_valid_payload(client: TestClient):
    login_as_demo(client)
    response = client.post("/api/ratings", json={"copy_id": 2, "rating": 4, "comment": "Desde tests"})
    assert response.status_code == 201, response.text
    payload = response.json()
    assert payload["copy_id"] == 2
    assert payload["rating"] == 4

    # rating fuera de rango se rechaza a nivel de validación
    bad = client.post("/api/ratings", json={"copy_id": 3, "rating": 10})
    assert bad.status_code == 422
