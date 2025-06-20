from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import database
from models import User
from routers.auth import get_current_user
from functions.teacher import get_my_students, get_students_test_results

teacher_router = APIRouter(tags=["Teacher"])

@teacher_router.get("/my_students")
def route_get_students(db: Session = Depends(database),
                       current_user: User = Depends(get_current_user)):
    return get_my_students(db, current_user)

@teacher_router.get("/my_students/results")
def route_get_test_results(db: Session = Depends(database),
                           current_user: User = Depends(get_current_user)):
    return get_students_test_results(db, current_user)
