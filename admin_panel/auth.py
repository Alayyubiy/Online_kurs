from passlib.context import CryptContext
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from datetime import datetime, timedelta
from jose import jwt, JWTError
from db import SessionLocal
from models.user import User
from routers.auth import SECRET_KEY, ALGORITHM


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


class AdminAuth(AuthenticationBackend):
    def init(self, secret_key: str):
        super().init(secret_key=secret_key)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()

            if not user:
                return False

            if not pwd_context.verify(password, user.password):
                return False

            if user.role != "admin":
                return False

            token = create_access_token({"sub": user.username})
            request.session.update({"token": token})
            return True
        finally:
            db.close()

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False

        try:
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return True
        except JWTError:
            return False