from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from db import database
from functions.student import get_my_students
from routers.auth import get_current_user

student_router = APIRouter(tags=["Student"])


@student_router.get("/my_students")
def route_get_my_students(db: Session = Depends(database),
                          current_user=Depends(get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Faqat teacher ko‘ra oladi")
    return get_my_students(db, current_user.id)
