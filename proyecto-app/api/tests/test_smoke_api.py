import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models
from app.db import Base, get_session
from app.main import app


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def client(test_engine):
    TestingSession = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)

    def override_session():
        session = TestingSession()
        try:
            yield session
            session.commit()
        finally:
            session.close()

    app.dependency_overrides[get_session] = override_session
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    with TestingSession() as session:
        book = models.Book(
            book_id=1,
            isbn="123",
            authors="Autor Demo",
            original_publication_year=2020,
            original_title="Libro Demo",
            title="Libro Demo",
            language_code="es",
            image_url=None,
        )
        copy = models.Copy(copy_id=1, book_id=1)
        user = models.User(user_id=1, full_name="Usuario Demo")
        rating = models.Rating(user_id=1, copy_id=1, rating=5)
        session.add_all([book, copy, user, rating])
        session.commit()

    yield TestClient(app)


def test_books_endpoint(client: TestClient):
    response = client.get("/books")
    assert response.status_code == 200
    payload = response.json()
    assert payload["items"], "Books response should not be empty"


def test_kpis_endpoint(client: TestClient):
    response = client.get("/kpis")
    assert response.status_code == 200
    payload = response.json()
    assert payload["books"] == 1
    assert payload["ratings"] == 1


def test_recommendations_endpoint(client: TestClient):
    response = client.get("/recommendations?m=10")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload[0]["score"] > 0
