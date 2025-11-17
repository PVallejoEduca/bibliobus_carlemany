import hashlib
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app import models
from app.db import Base, get_session
from app.main import app


def seed_sample_data(session: Session) -> None:
    books = [
        models.Book(
            book_id=1,
            isbn="ISBN-001",
            authors="Autor Uno",
            original_publication_year=2000,
            original_title="Libro Uno",
            title="Libro Uno",
            language_code="es",
            image_url=None,
        ),
        models.Book(
            book_id=2,
            isbn="ISBN-002",
            authors="Autor Dos",
            original_publication_year=2010,
            original_title="Libro Dos",
            title="Libro Dos",
            language_code="en",
            image_url=None,
        ),
    ]
    copies = [
        models.Copy(copy_id=1, book_id=1),
        models.Copy(copy_id=2, book_id=1),
        models.Copy(copy_id=3, book_id=2),
    ]
    users = [
        models.User(user_id=1, full_name="Usuario Uno", email="uno@example.com"),
        models.User(user_id=2, full_name="Usuario Dos", email="dos@example.com"),
    ]
    logins = [
        models.UserLogin(
            user_id=1,
            nickname="demo",
            password_hash=hashlib.md5(b"demo").hexdigest(),
        ),
        models.UserLogin(
            user_id=2,
            nickname="tester",
            password_hash=hashlib.md5(b"tester").hexdigest(),
        ),
    ]
    ratings = [
        models.Rating(user_id=1, copy_id=1, rating=5, comment="Genial"),
        models.Rating(user_id=2, copy_id=2, rating=4, comment="Muy bueno"),
        models.Rating(user_id=1, copy_id=3, rating=3, comment="Normal"),
    ]
    session.add_all(books + copies + users + logins + ratings)
    session.commit()


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="session")
def session_factory(engine):
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def reset_database(engine, session_factory):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = session_factory()
    seed_sample_data(session)
    session.close()


@pytest.fixture
def db_session(engine, session_factory) -> Generator[Session, None, None]:
    reset_database(engine, session_factory)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(engine, session_factory):
    reset_database(engine, session_factory)

    def override_session():
        session = session_factory()
        try:
            yield session
            session.commit()
        finally:
            session.close()

    app.dependency_overrides[get_session] = override_session
    return TestClient(app)
