from ..repositories.books_repo import BooksRepository


class BooksService:
    """Orquesta catalogo de libros."""

    def __init__(self, repo: BooksRepository):
        self.repo = repo

    def list_books(self, limit: int, offset: int, query: str | None, language: str | None, category: str | None):
        items = self.repo.list_books(limit, offset, query, language, category)
        total = self.repo.count_books(query, language, category)
        return {
            "items": [
                self._serialize_book(b)
                for b in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    def get_book(self, book_id: int):
        book = self.repo.get_book(book_id)
        if not book:
            return None
        return self._serialize_book(book)

    def get_copies(self, book_id: int):
        copies = self.repo.list_copies(book_id)
        return [{"copy_id": c.copy_id} for c in copies]

    @staticmethod
    def _serialize_book(book):
        return {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.authors,
            "language": book.language_code,
            "category": None,
            "published_year": book.original_publication_year,
            "image_url": book.image_url,
        }
