from fastapi.testclient import TestClient


def test_books_endpoint(client: TestClient):
    response = client.get("/api/books")
    assert response.status_code == 200
    payload = response.json()
    assert payload["items"], "Books response should not be empty"


def test_kpis_endpoint(client: TestClient):
    response = client.get("/api/kpis")
    assert response.status_code == 200
    payload = response.json()
    assert payload["books"] >= 1
    assert payload["ratings"] >= 1


def test_recommendations_endpoint(client: TestClient):
    response = client.get("/api/recommendations?m=10")
    assert response.status_code == 200
    payload = response.json()
    assert "items" in payload and payload["items"], "Debe devolver recomendaciones"
    assert payload["items"][0]["score"] > 0


def test_health_like_endpoint(client: TestClient):
    """Basic smoke to ensure the API serves HTML landing page."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Bibliobus" in response.text
