import time

from fastapi.testclient import TestClient


def test_recommendations_endpoint_performance(client: TestClient):
    attempts = 5
    durations = []
    for _ in range(attempts):
        start = time.perf_counter()
        resp = client.get("/api/recommendations?m=10")
        end = time.perf_counter()
        assert resp.status_code == 200
        durations.append(end - start)
    avg = sum(durations) / len(durations)
    assert avg < 2.0, f"Latencia media demasiado alta: {avg}"
