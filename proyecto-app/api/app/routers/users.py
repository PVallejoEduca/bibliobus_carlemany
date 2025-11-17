from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db import get_session
from ..repositories.users_repo import UsersRepository

router = APIRouter(prefix="/users", tags=["users"])


class UserDetail(BaseModel):
    user_id: int
    full_name: str | None = None
    email: str | None = None
    member_since: str | None = None
    nickname: str | None = None


@router.get("/{user_id}", response_model=UserDetail)
def get_user(user_id: int, session: Session = Depends(get_session)):
    repo = UsersRepository(session)
    user = repo.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user_not_found")
    return {
        "user_id": user.user_id,
        "full_name": user.full_name,
        "email": user.email,
        "member_since": user.member_since.isoformat() if user.member_since else None,
        "nickname": user.login.nickname if user.login else None,
    }
