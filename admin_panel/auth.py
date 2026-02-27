from passlib.context import CryptContext
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from datetime import datetime, timedelta
from jose import jwt, JWTError
from db import SessionLocal
from models.user import User
from routers.auth import SECRET_KEY, ALGORITHM


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=60)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


class AdminAuth(AuthenticationBackend):

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username", "")
        password = form.get("password", "")

        # ✅ Bo'sh input tekshiruvi
        if not username or not password:
            return False

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()

            # ✅ Timing attack himoya: user topilmasa ham verify chaqiriladi
            if user:
                is_valid = pwd_context.verify(password, user.password)
            else:
                pwd_context.dummy_verify()
                is_valid = False

            if not is_valid:
                return False

            # ✅ Faqat admin role ga ruxsat
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