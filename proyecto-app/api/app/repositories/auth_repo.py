from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .. import models


class AuthRepository:
    """Acceso a credenciales de usuarios."""

    def __init__(self, session: Session):
        self.session = session

    def get_login_by_nickname(self, nickname: str):
        stmt = (
            select(models.UserLogin)
            .join(models.User)
            .where(func.lower(models.UserLogin.nickname) == nickname.lower())
        )
        return self.session.execute(stmt).scalar_one_or_none()
