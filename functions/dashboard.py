
from models import User, Course, Lesson, Enrollment
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models import  Progress
from models.payments import Payment
from models.test_history import TestHistory


def get_summary_stats(db: Session):
    total_users = db.query(func.count(User.id)).scalar()
    total_courses = db.query(func.count(Course.id)).scalar()
    total_lessons = db.query(func.count(Lesson.id)).scalar()
    total_enrollments = db.query(func.count(Enrollment.id)).scalar()

    return {
        "total_users": total_users,
        "total_courses": total_courses,
        "total_lessons": total_lessons,
        "total_enrollments": total_enrollments
    }


def get_top_students(db: Session, limit: int = 5):
    result = (
        db.query(
            TestHistory.user_id,
            func.avg(TestHistory.score).label("avg_score"),
            User.name
        )
        .join(User, User.id == TestHistory.user_id)
        .group_by(TestHistory.user_id, User.name)
        .order_by(desc("avg_score"))
        .limit(limit)
        .all()
    )

    return [
        {"user_id": row.user_id, "name": row.name, "avg_score": round(row.avg_score, 2)}
        for row in result
    ]


def get_lowest_students(db: Session, limit: int = 5):
    result = (
        db.query(
            TestHistory.user_id,
            func.avg(TestHistory.score).label("avg_score"),
            User.name
        )
        .join(User, User.id == TestHistory.user_id)
        .group_by(TestHistory.user_id, User.name)
        .order_by(func.avg(TestHistory.score))  # pastdan yuqoriga
        .limit(limit)
        .all()
    )

    return [
        {"user_id": row.user_id, "name": row.name, "avg_score": round(row.avg_score, 2)}
        for row in result
    ]


# umumiy uquvchilar haqida malumotni kurish uchun


def get_admin_dashboard(db):
    total_users = db.query(User).count()
    total_courses = db.query(Course).count()
    total_lessons = db.query(Lesson).count()
    total_payments = db.query(Payment).count()

    total_paid_amount = db.query(func.sum(Payment.amount)).filter(Payment.status == "paid").scalar() or 0
    total_paid_users = db.query(Payment.user_id).filter(Payment.status == "paid").distinct().count()

    top_students = (
        db.query(Progress.user_id, func.count(Progress.lesson_id).label("completed_lessons"))
        .filter(Progress.completed == True)
        .group_by(Progress.user_id)
        .order_by(func.count(Progress.lesson_id).desc())
        .limit(5)
        .all()
    )

    return {
        "total_users": total_users,
        "total_courses": total_courses,
        "total_lessons": total_lessons,
        "total_payments": total_payments,
        "total_paid_amount": total_paid_amount,
        "total_paid_users": total_paid_users,
        "top_students": [
            {"user_id": u[0], "completed_lessons": u[1]} for u in top_students
        ]
    }
