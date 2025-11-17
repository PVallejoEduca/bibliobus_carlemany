from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..auth_utils import COOKIE_NAME
from ..db import get_session
from ..domain.auth_service import AuthService
from ..repositories.auth_repo import AuthRepository

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginPayload(BaseModel):
    nickname: str
    password: str


class LoginResponse(BaseModel):
    user_id: int
    full_name: str
    nickname: str


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginPayload, response: Response, session: Session = Depends(get_session)):
    service = AuthService(AuthRepository(session))
    try:
        user = service.login(payload.nickname, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="credenciales_invalidas") from exc
    response.set_cookie(key=COOKIE_NAME, value=str(user["user_id"]), httponly=True, samesite="lax")
    return user


@router.post("/logout", status_code=204)
def logout(response: Response):
    response.delete_cookie(COOKIE_NAME)
    return Response(status_code=204)
