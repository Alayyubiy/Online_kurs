from fastapi import FastAPI
from db import engine, Base
from routers.auth import login_router
from routers.courses import courses_router
from routers.user import user_router
from routers.section import section_router
from routers.lesson import lesson_router
from routers.progress import progress_router
from  routers.enrollments import enrollment_router
from routers.quiz import quiz_router
from routers.test_history import test_history_router

app = FastAPI(docs_url='/', title="ONLINEKURS")

Base.metadata.create_all(bind=engine)

app.include_router(courses_router)
app.include_router(section_router)
app.include_router(lesson_router)
app.include_router(progress_router)
app.include_router(enrollment_router)
app.include_router(quiz_router)
app.include_router(test_history_router)
app.include_router(user_router)
app.include_router(login_router)



