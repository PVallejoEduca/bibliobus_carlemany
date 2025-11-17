from app import models
from app.repositories.books_repo import BooksRepository


def test_books_list_always_has_copies(db_session):
    repo = BooksRepository(db_session)
    books = repo.list_books(limit=20, offset=0, query=None, language=None, category=None)
    assert books, "Seed data should include libros"
    for book in books:
        copies = repo.list_copies(book.book_id)
        assert copies, f"Book {book.book_id} debe tener ejemplares asociados"


def test_ratings_reference_existing_copies(db_session):
    copy_ids = {copy.copy_id for copy in db_session.query(models.Copy).all()}
    orphan_ratings = [
        rating.rating_id
        for rating in db_session.query(models.Rating).all()
        if rating.copy_id not in copy_ids
    ]
    assert not orphan_ratings, f"Existen ratings huérfanos: {orphan_ratings}"
