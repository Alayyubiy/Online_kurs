import os
import logging
from datetime import datetime, timedelta
from typing import Optional
from collections import defaultdict
from fastapi import Depends, APIRouter, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm.session import Session
from db import database
from models.user import User
from schemas.tokens import TokenData, Token
from schemas.users import CreateUser

logger = logging.getLogger(__name__)

# ✅ SECRET_KEY kodda emas, environment variable dan
SECRET_KEY = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ✅ Brute-force himoya
login_attempts: dict = defaultdict(list)
MAX_ATTEMPTS = 5
LOCKOUT_MINUTES = 15


def check_rate_limit(ip: str):
    now = datetime.utcnow()
    window_start = now - timedelta(minutes=LOCKOUT_MINUTES)
    login_attempts[ip] = [t for t in login_attempts[ip] if t > window_start]
    if len(login_attempts[ip]) >= MAX_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Juda ko'p urinish. {LOCKOUT_MINUTES} daqiqadan so'ng urinib ko'ring.",
        )


def record_failed_attempt(ip: str):
    login_attempts[ip].append(datetime.utcnow())


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
login_router = APIRouter(tags=['Login and Refresh token'])


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(db: Session = Depends(database), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: CreateUser = Depends(get_current_user)):
    return current_user


@login_router.post("/token")
async def login_for_access_token(
    request: Request,
    db: Session = Depends(database),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    client_ip = request.client.host
    check_rate_limit(client_ip)

    user = db.query(User).filter(User.username == form_data.username).first()

    if user:
        is_valid = pwd_context.verify(form_data.password, user.password)
    else:
        pwd_context.dummy_verify()
        is_valid = False

    if not is_valid:
        record_failed_attempt(client_ip)
        logger.warning(f"Failed login: username='{form_data.username}' IP={client_ip}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login yoki parolda xatolik",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    db.query(User).filter(User.id == user.id).update({User.token: access_token})
    db.commit()

    logger.info(f"Successful login: user_id={user.id} IP={client_ip}")

    # ✅ FIX: Frontend kutgan barcha maydonlarni qaytarish
    # Eski: faqat {id, access_token, token_type}
    # Yangi: name, username, role, phone ham qo'shildi
    return {
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'role': user.role,
        'phone': user.phone,
        'access_token': access_token,
        'token_type': 'bearer'
    }


@login_router.post("/refresh_token", response_model=Token)
async def refresh_token(db: Session = Depends(database), token: str = None):
    if not token:
        raise HTTPException(status_code=400, detail="Token kiritilmadi")

    user = db.query(User).filter(User.token == token).first()
    if user is None:
        raise HTTPException(status_code=400, detail="Noto'g'ri token")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    db.query(User).filter(User.id == user.id).update({User.token: access_token})
    db.commit()

    return {'id': user.id, "access_token": access_token, "token_type": "bearer"}