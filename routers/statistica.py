# routers/statistics.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import asc, func
from sqlalchemy.orm import Session
from db import database
from models.test_history import TestHistory
from models.user import User
from routers.auth import get_current_user
from services.statistica import get_user_scores_chart_data

statistics_router = APIRouter(tags=["Statistics"])

@statistics_router.get("/my_score_chart")
def my_score_chart(
    db: Session = Depends(database),
    current_user: User = Depends(get_current_user)
):
    return get_user_scores_chart_data(current_user, db)

@statistics_router.get("/worst_students")
def get_worst_students(db: Session = Depends(database),
                       current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Faqat adminlar ko'rishi mumkin.")

    result = (
        db.query(
            TestHistory.user_id,
            func.avg(TestHistory.score).label("avg_score"),
            User.name
        )
        .join(User, User.id == TestHistory.user_id)
        .group_by(TestHistory.user_id)
        .order_by(asc("avg_score"))
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
