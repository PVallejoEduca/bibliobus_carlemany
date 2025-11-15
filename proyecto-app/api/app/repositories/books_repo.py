from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from .. import models


class BooksRepository:

    def __init__(self, session: Session):
        self.session = session

    def _apply_filters(self, stmt, query: str | None, language: str | None, category: str | None):
        if query:
            pattern = f"%{query}%"
            stmt = stmt.where(
                or_(
                    models.Book.title.ilike(pattern),
                    models.Book.authors.ilike(pattern),
                    models.Book.original_title.ilike(pattern),
                )
            )
        if language:
            stmt = stmt.where(models.Book.language_code == language)
        if category:
            # Schema actual no tiene columna de categoría; se ignora filtro para compatibilidad
            pass
        return stmt

    def list_books(self, limit: int, offset: int, query: str | None, language: str | None, category: str | None):
        stmt = select(models.Book).order_by(models.Book.title)
        stmt = self._apply_filters(stmt, query, language, category)
        stmt = stmt.offset(offset).limit(limit)
        return list(self.session.scalars(stmt))

    def count_books(self, query: str | None, language: str | None, category: str | None) -> int:
        stmt = select(func.count(models.Book.book_id))
        stmt = self._apply_filters(stmt, query, language, category)
        return self.session.execute(stmt).scalar_one()

    def get_book(self, book_id: int):
        return self.session.get(models.Book, book_id)

    def list_copies(self, book_id: int):
        stmt = (
            select(models.Copy)
            .where(models.Copy.book_id == book_id)
            .order_by(models.Copy.copy_id)
        )
        return list(self.session.scalars(stmt))
