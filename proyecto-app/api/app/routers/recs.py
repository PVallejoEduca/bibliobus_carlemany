from fastapi import APIRouter, Depends, Query
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


@router.get("/", response_model=list[RecommendationOut])
def get_recommendations(m: int = Query(50, ge=1, le=500), session: Session = Depends(get_session)):
    service = RecsService(RatingsRepository(session))
    recs = service.top_global(m=m)
    return [r.__dict__ for r in recs]
