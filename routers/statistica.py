# routers/statistics.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import database
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
