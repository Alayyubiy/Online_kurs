from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from admin_panel.user import UserAdmin
from db import engine, Base
from routers.auth import login_router, SECRET_KEY
from routers.courses import courses_router
from routers.user import user_router
from routers.section import section_router
from routers.lesson import lesson_router
from routers.progress import progress_router
from admin_panel.auth import AdminAuth
from admin_panel.section import SectionAdmin
from admin_panel.lesson import LessonAdmin
from admin_panel.course import CourseAdmin
from admin_panel.payments import PaymentAdmin
from routers.payments import payment_router




app = FastAPI(docs_url='/', title="ONLINEKURS")

origins = [
    "http://localhost:5173",     # Vite (React) uchun
    "http://127.0.0.1:5173",     # Ba’zan localhost o‘rniga shu bo‘ladi
    "https://bf2a6cf2df8c.ngrok-free.app",
    "https://12ce-185-213-229-97.ngrok-free.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


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
app.include_router(progress_router)
app.include_router(payment_router)
app.include_router(user_router)
app.include_router(login_router)



