from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_session
from ..domain.kpis_service import KpisService
from ..repositories.ratings_repo import RatingsRepository

router = APIRouter(prefix="/kpis", tags=["kpis"])


@router.get("/", response_model=dict)
def get_kpis(session: Session = Depends(get_session)):
    service = KpisService(RatingsRepository(session))
    return service.get_kpis()
