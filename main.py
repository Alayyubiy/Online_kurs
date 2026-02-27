import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from admin_panel.user import UserAdmin
from db import engine, Base
from routers.auth import login_router, SECRET_KEY
from routers.courses import courses_router
from routers.user import user_router
from routers.section import section_router
from routers.lesson import lesson_router
from admin_panel.auth import AdminAuth
from admin_panel.section import SectionAdmin
from admin_panel.lesson import LessonAdmin
from admin_panel.course import CourseAdmin
from admin_panel.payments import PaymentAdmin
from routers.payments import payment_router
from dotenv import load_dotenv

load_dotenv()

# ✅ FIX: Production da docs_url=None qiling (API docs ni yashirish)
# Development uchun: docs_url='/'
IS_PRODUCTION = os.getenv("ENVIRONMENT", "development") == "production"

app = FastAPI(
    title="ONLINEKURS",
    docs_url=None if IS_PRODUCTION else "/",      # ✅ Production da Swagger yashirish
    redoc_url=None if IS_PRODUCTION else "/redoc",
    openapi_url=None if IS_PRODUCTION else "/openapi.json",
)

# ✅ FIX: CORS - aniq domainlar ko'rsatish, ["*"] XAVFLI!
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

# Development uchun localhost qo'shish
if not IS_PRODUCTION:
    ALLOWED_ORIGINS.extend([
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,        # ✅ ["*"] emas, aniq domenlar!
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # ✅ Faqat kerakli methodlar
    allow_headers=["Authorization", "Content-Type"],  # ✅ Faqat kerakli headerlar
)

# ✅ FIX: Faqat o'z domeningizdan so'rov qabul qilish
if IS_PRODUCTION:
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "yourdomain.com").split(",")
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)

# ✅ FIX: SECRET_KEY .env dan olish kerak
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


# ✅ FIX: Security headers qo'shish (XSS, Clickjacking himoya)
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if IS_PRODUCTION:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "object-src 'none';"
        )
    return response


# ✅ FIX: Xato xabarlarini foydalanuvchiga ko'rsatmaslik
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Ichki server xatosi yuz berdi"}
    )


authentication_backend = AdminAuth(secret_key=SECRET_KEY)
admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_model_view(UserAdmin)
admin.add_model_view(CourseAdmin)
admin.add_model_view(SectionAdmin)
admin.add_model_view(LessonAdmin)
admin.add_model_view(PaymentAdmin)

Base.metadata.create_all(bind=engine)

app.include_router(courses_router)
app.include_router(section_router)
app.include_router(lesson_router)
app.include_router(payment_router)
app.include_router(user_router)
app.include_router(login_router)