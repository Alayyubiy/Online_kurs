from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Lesson, Enrollment, User
from models.test_history import TestHistory

def get_my_students(db: Session, current_user: User):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Faqat teacherlar ko‘ra oladi.")

    lessons = db.query(Lesson).filter(Lesson.created_by == current_user.id).all()
    lesson_ids = [lesson.id for lesson in lessons]

    enrollments = db.query(Enrollment).filter(Enrollment.course_id.in_(lesson_ids)).all()
    student_ids = list(set(enr.user_id for enr in enrollments))

    students = db.query(User).filter(User.id.in_(student_ids)).all()
    return students


def get_students_test_results(db: Session, current_user: User):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Faqat teacherlar uchun")

    lessons = db.query(Lesson).filter(Lesson.created_by == current_user.id).all()
    lesson_ids = [lesson.id for lesson in lessons]

    histories = db.query(TestHistory).filter(TestHistory.lesson_id.in_(lesson_ids)).all()
    return histories
