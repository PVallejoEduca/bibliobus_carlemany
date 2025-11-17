from fastapi import Cookie, HTTPException

COOKIE_NAME = "bibliobus_user"


def require_user_id(user_cookie: str | None = Cookie(default=None, alias=COOKIE_NAME)):
    if user_cookie is None:
        raise HTTPException(status_code=401, detail="login_requerido")
    try:
        return int(user_cookie)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=401, detail="login_requerido") from exc
