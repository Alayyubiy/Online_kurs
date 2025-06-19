from models.test_history import TestHistory
from models.user import User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import func, desc


def get_user_test_history(db: Session, current_user):
    return db.query(TestHistory).filter(TestHistory.user_id == current_user.id).all()


def get_test_history_by_user(user_id: int, db: Session):
    return db.query(TestHistory).filter(TestHistory.user_id == user_id).all()


def get_top_students(db: Session):
    result = (
        db.query(
            TestHistory.user_id,
            func.avg(TestHistory.score).label("avg_score"),
            User.name
        )
        .join(User, User.id == TestHistory.user_id)
        .group_by(TestHistory.user_id, User.name)  # name ham group_by ga qo‘shiladi
        .order_by(desc("avg_score"))
        .limit(10)
        .all()
    )

    return [
        {
            "user_id": row.user_id,
            "name": row.name,
            "avg_score": round(row.avg_score, 2) if row.avg_score is not None else 0.0
        }
        for row in result
    ]


def delete_test_history(ident: int, db, current_user):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Faqat adminlar o‘chira oladi.")

    history = db.query(TestHistory).filter(TestHistory.id == ident).first()
    if not history:
        raise HTTPException(status_code=404, detail="Bunday test tarixi topilmadi.")

    db.delete(history)
    db.commit()
    return {"message": "Test tarixi muvaffaqiyatli o‘chirildi."}