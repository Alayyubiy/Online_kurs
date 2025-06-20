from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.test_history import TestHistory
from models.user import User
from models.lesson import Lesson
from sqlalchemy import func, desc

def get_user_test_history(db: Session, current_user: User):
    return db.query(TestHistory).filter_by(user_id=current_user.id).all()

def get_test_history_by_user(user_id: int, db: Session, current_user: User):
    if current_user.role == "admin":
        return db.query(TestHistory).filter(TestHistory.user_id == user_id).all()
    elif current_user.role == "teacher":
        return db.query(TestHistory).join(Lesson).filter(
            Lesson.created_by == current_user.id,
            TestHistory.user_id == user_id
        ).all()
    else:
        raise HTTPException(status_code=403, detail="Sizda ruxsat yo'q.")

def get_top_students(db: Session, current_user: User):
    query = db.query(
        TestHistory.user_id,
        func.avg(TestHistory.score).label("avg_score"),
        User.name
    ).join(User, User.id == TestHistory.user_id)

    if current_user.role == "teacher":
        query = query.join(Lesson, Lesson.id == TestHistory.lesson_id).filter(
            Lesson.created_by == current_user.id
        )

    result = (
        query.group_by(TestHistory.user_id)
        .order_by(desc("avg_score"))
        .limit(10)
        .all()
    )

    return [
        {
            "user_id": row.user_id,
            "name": row.name,
            "avg_score": round(row.avg_score, 2)
        }
        for row in result
    ]

def delete_test_history(ident: int, db: Session, current_user: User):
    history = db.query(TestHistory).filter_by(id=ident).first()
    if not history:
        raise HTTPException(status_code=404, detail="Tarix topilmadi.")

    # Teacher faqat o‘z darslariga tegishli tarixni o‘chirishi mumkin
    if current_user.role == "teacher":
        lesson = db.query(Lesson).filter(Lesson.id == history.lesson_id).first()
        if lesson.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="Bu tarix sizga tegishli emas.")
    elif current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Sizda ruxsat yo‘q.")

    db.delete(history)
    db.commit()
    return {"message": "Test tarixi o‘chirildi."}
