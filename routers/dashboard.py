from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import database
from routers.auth import get_current_user
from models import User
from functions.dashboard import get_summary_stats

dashboard_router = APIRouter(tags=["Dashboard"])
# Bu hamma malumotlarni admin kurishi uchun

@dashboard_router.get("/dashboard/summary")
def dashboard_summary(
        db: Session = Depends(database),
        current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Faqat adminlar uchun")

    return get_summary_stats(db)


from functions.dashboard import get_top_students


@dashboard_router.get("/dashboard/top-students")
def dashboard_top_students(
        db: Session = Depends(database),
        current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Faqat adminlar uchun")

    return get_top_students(db)


from functions.dashboard import get_lowest_students


@dashboard_router.get("/dashboard/lowest-students")
def dashboard_lowest_students(
        db: Session = Depends(database),
        current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Faqat adminlar uchun")

    return get_lowest_students(db)

