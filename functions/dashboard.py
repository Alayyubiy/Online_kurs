
from models import User, Course, Lesson, Enrollment
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
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
