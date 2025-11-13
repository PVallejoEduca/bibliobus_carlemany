import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://app:app@localhost:5432/libdb")

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, class_=Session)


class Base(DeclarativeBase):
    """Base SQLAlchemy declarative class."""


def get_session():
    """Yield a database session for FastAPI dependencies."""
    session = SessionLocal()
    bind = session.get_bind()
    if bind and bind.dialect.name == "postgresql":
        session.execute(text("SET search_path TO lib, public"))
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
