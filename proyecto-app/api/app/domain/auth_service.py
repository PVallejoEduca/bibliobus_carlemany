import hashlib

from ..repositories.auth_repo import AuthRepository


class AuthService:
    """Valida credenciales básicas."""

    def __init__(self, repo: AuthRepository):
        self.repo = repo

    def login(self, nickname: str, password: str):
        login = self.repo.get_login_by_nickname(nickname)
        if not login or not login.user:
            raise ValueError("credenciales_invalidas")
        hashed = hashlib.md5(password.encode("utf-8")).hexdigest()
        if hashed.lower() != (login.password_hash or "").lower():
            raise ValueError("credenciales_invalidas")
        user = login.user
        return {
            "user_id": user.user_id,
            "full_name": user.full_name,
            "nickname": login.nickname,
        }
