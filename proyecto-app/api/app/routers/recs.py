from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db import get_session
from ..domain.recs_service import RecsService
from ..repositories.ratings_repo import RatingsRepository

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


class RecommendationOut(BaseModel):
    book_id: int
    title: str
    score: float
    ratings: int


class RecommendationPage(BaseModel):
    items: list[RecommendationOut]
    total: int
    limit: int
    offset: int


@router.get("/", response_model=RecommendationPage)
def get_recommendations(
    m: int = Query(50, ge=1, le=500),
    limit: int = Query(9, ge=1, le=200),
    page: int = Query(1, ge=1),
    session: Session = Depends(get_session),
):
    service = RecsService(RatingsRepository(session))
    recs = service.top_global(m=m)
    total = len(recs)
    offset = (page - 1) * limit
    items = recs[offset: offset + limit] if offset < total else []
    return {
        "items": [r.__dict__ for r in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/hidden", response_model=RecommendationPage)
def get_hidden_gems(
    limit: int = Query(9, ge=1, le=50),
    page: int = Query(1, ge=1),
    min_votes: int = Query(1, ge=1),
    max_votes: int = Query(10, ge=1),
    min_avg: float = Query(4.5, ge=1.0, le=5.0),
    session: Session = Depends(get_session),
):
    if min_votes > max_votes:
        raise HTTPException(status_code=400, detail="min_votes_no_puede_ser_mayor_que_max_votes")
    service = RecsService(RatingsRepository(session))
    gems = service.hidden_gems(min_votes=min_votes, max_votes=max_votes, min_avg=min_avg)
    total = len(gems)
    offset = (page - 1) * limit
    items = gems[offset : offset + limit] if offset < total else []
    return {
        "items": [g.__dict__ for g in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }
