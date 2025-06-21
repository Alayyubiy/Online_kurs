from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware
from admin_panel.test_history import HistoryAdmin
from admin_panel.user import UserAdmin
from db import engine, Base
from routers.auth import login_router, SECRET_KEY
from routers.courses import courses_router
from routers.user import user_router
from routers.section import section_router
from routers.lesson import lesson_router
from routers.progress import progress_router
from routers.student import student_router
from routers.dashboard import dashboard_router
from  routers.enrollments import enrollment_router
from routers.quiz import quiz_router
from routers.test_history import test_history_router
from routers.statistica import statistics_router
from routers.teacher import teacher_router
from admin_panel.auth import AdminAuth
from admin_panel.section import SectionAdmin
from admin_panel.quiz import QuizAdmin
from admin_panel.lesson import LessonAdmin
from admin_panel.enrollment import EnrollmentAdmin
from admin_panel.course import CourseAdmin
from admin_panel.payments import PaymentAdmin
from routers.payments import payment_router



app = FastAPI(docs_url='/', title="ONLINEKURS")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


authentication_backend = AdminAuth(secret_key=SECRET_KEY)
admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_model_view(UserAdmin)
admin.add_model_view(EnrollmentAdmin)
admin.add_model_view(CourseAdmin)
admin.add_model_view(SectionAdmin)
admin.add_model_view(LessonAdmin)
admin.add_model_view(HistoryAdmin)
admin.add_model_view(QuizAdmin)
admin.add_model_view(PaymentAdmin)



Base.metadata.create_all(bind=engine)

app.include_router(courses_router)
app.include_router(section_router)
app.include_router(lesson_router)
app.include_router(progress_router)
app.include_router(enrollment_router)
app.include_router(quiz_router)
app.include_router(test_history_router)
app.include_router(statistics_router)
app.include_router(teacher_router)
app.include_router(student_router)
app.include_router(dashboard_router)
app.include_router(payment_router)
app.include_router(user_router)
app.include_router(login_router)



