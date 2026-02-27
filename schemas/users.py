import re
from pydantic import BaseModel, Field, validator


def validate_password_strength(password: str) -> str:
    """
    ✅ FIX: Kuchli parol talablari
    Eski kod: min_length=4, max_length=8 - BU JUDA ZAIF!
    """
    if len(password) < 8:
        raise ValueError("Parol kamida 8 ta belgidan iborat bo'lishi kerak")
    if len(password) > 128:
        raise ValueError("Parol 128 ta belgidan oshmasligi kerak")
    if not re.search(r'[A-Z]', password):
        raise ValueError("Parolda kamida 1 ta katta harf bo'lishi kerak")
    if not re.search(r'[a-z]', password):
        raise ValueError("Parolda kamida 1 ta kichik harf bo'lishi kerak")
    if not re.search(r'\d', password):
        raise ValueError("Parolda kamida 1 ta raqam bo'lishi kerak")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError("Parolda kamida 1 ta maxsus belgi (!@#$%^&* va h.k.) bo'lishi kerak")
    return password


def validate_username(username: str) -> str:
    """✅ FIX: Username validatsiyasi - XSS va injection oldini olish"""
    if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
        raise ValueError("Username faqat harf, raqam, _ . - belgilardan iborat bo'lishi kerak")
    if len(username) < 3:
        raise ValueError("Username kamida 3 ta belgidan iborat bo'lishi kerak")
    if len(username) > 50:
        raise ValueError("Username 50 ta belgidan oshmasligi kerak")
    return username.lower()


def validate_phone(phone: str) -> str:
    """✅ FIX: Telefon raqam validatsiyasi"""
    phone_clean = re.sub(r'[\s\-\(\)]', '', phone)
    if not re.match(r'^\+?[0-9]{9,15}$', phone_clean):
        raise ValueError("Telefon raqam noto'g'ri formatda (masalan: +998901234567)")
    return phone_clean


class CreateUser(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    username: str = Field(min_length=3, max_length=50)
    password: str  # ✅ FIX: min=4, max=8 dan kuchliroq validatsiyaga o'tish
    phone: str

    @validator('password')
    def password_strength(cls, v):
        return validate_password_strength(v)

    @validator('username')
    def username_valid(cls, v):
        return validate_username(v)

    @validator('phone')
    def phone_valid(cls, v):
        return validate_phone(v)

    @validator('name')
    def name_valid(cls, v):
        # XSS belgilarini tozalash
        v = v.strip()
        if re.search(r'[<>&"\'\/\\]', v):
            raise ValueError("Ism noto'g'ri belgilar o'z ichiga olgan")
        return v


class UpdateUser(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    username: str = Field(min_length=3, max_length=50)
    password: str
    phone: str

    @validator('password')
    def password_strength(cls, v):
        return validate_password_strength(v)

    @validator('username')
    def username_valid(cls, v):
        return validate_username(v)

    @validator('phone')
    def phone_valid(cls, v):
        return validate_phone(v)


class CreateStudent(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    username: str = Field(min_length=3, max_length=50)
    password: str
    phone: str

    @validator('password')
    def password_strength(cls, v):
        return validate_password_strength(v)