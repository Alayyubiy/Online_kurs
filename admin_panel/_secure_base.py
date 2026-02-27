from sqladmin import ModelView
from starlette.requests import Request
from jose import jwt, JWTError
from routers.auth import SECRET_KEY, ALGORITHM


class SecureAdminView(ModelView):
    """Barcha admin view lar shu sinfdan meros oladi"""

    def is_accessible(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        try:
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return True
        except JWTError:
            return False

    def is_visible(self, request: Request) -> bool:
        return self.is_accessible(request)