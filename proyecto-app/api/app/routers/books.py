from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db import get_session
from ..domain.books_service import BooksService
from ..repositories.books_repo import BooksRepository

router = APIRouter(prefix="/books", tags=["books"])


class BookItem(BaseModel):
    book_id: int
    title: str
    author: str | None = None
    language: str | None = None
    category: str | None = None
    image_url: str | None = None
    published_year: int | None = None


class PaginatedBooks(BaseModel):
    items: list[BookItem]
    total: int
    limit: int
    offset: int


class BookDetail(BookItem):
    pass


class CopyItem(BaseModel):
    copy_id: int
    location: str | None = None
    status: str | None = None
    inventory_code: str | None = None


@router.get("/", response_model=PaginatedBooks)
def list_books(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    q: str | None = Query(default=None, min_length=1),
    language: str | None = Query(default=None),
    category: str | None = Query(default=None),
    session: Session = Depends(get_session),
):
    service = BooksService(BooksRepository(session))
    return service.list_books(limit=limit, offset=offset, query=q, language=language, category=category)


@router.get("/{book_id}", response_model=BookDetail)
def get_book(book_id: int, session: Session = Depends(get_session)):
    service = BooksService(BooksRepository(session))
    book = service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book_not_found")
    return book


@router.get("/{book_id}/copies", response_model=list[CopyItem])
def get_copies(book_id: int, session: Session = Depends(get_session)):
    service = BooksService(BooksRepository(session))
    copies = service.get_copies(book_id)
    if not copies and service.get_book(book_id) is None:
        raise HTTPException(status_code=404, detail="book_not_found")
    return copies
