from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..auth_utils import require_user_id
from ..db import get_session
from ..domain.ratings_service import RatingsService
from ..repositories.ratings_repo import RatingsRepository

router = APIRouter(prefix="/ratings", tags=["ratings"])


class RatingCreate(BaseModel):
    copy_id: int = Field(ge=1)
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None, max_length=500)


class RatingOut(BaseModel):
    rating_id: int
    user_id: int
    copy_id: int
    rating: int
    comment: str | None = None


@router.post("/", response_model=RatingOut, status_code=201)
def create_rating(
    payload: RatingCreate,
    current_user_id: int = Depends(require_user_id),
    session: Session = Depends(get_session),
):
    service = RatingsService(RatingsRepository(session))
    try:
        rating = service.add_rating(current_user_id, payload.copy_id, payload.rating, payload.comment)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return rating


@router.get("/", response_model=list[RatingOut])
def list_ratings(
    book_id: int | None = Query(default=None, ge=1),
    user_id: int | None = Query(default=None, ge=1),
    session: Session = Depends(get_session),
):
    service = RatingsService(RatingsRepository(session))
    return service.list_ratings(book_id=book_id, user_id=user_id)
