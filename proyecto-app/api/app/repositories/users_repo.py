from sqlalchemy.orm import Session

from .. import models


class UsersRepository:
    """Consultas básicas de usuarios."""

    def __init__(self, session: Session):
        self.session = session

    def get_user(self, user_id: int):
        return self.session.get(models.User, user_id)
