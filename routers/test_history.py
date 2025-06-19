from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import database
from models.test_history import TestHistory
from schemas.test_history import TestHistoryOut, TopStudentOut
from functions.test_history import (
    get_user_test_history,
    get_test_history_by_user,
    get_top_students,
    delete_test_history
)
from routers.auth import get_current_user
from models.user import User

test_history_router = APIRouter(tags=["Test History"])


# ✅ 1. Shaxsiy test tarixini olish yoki barcha tarixni olish (admin bo‘lsa)
@test_history_router.get("/test_histories", response_model=list[TestHistoryOut])
def route_get_test_history(db: Session = Depends(database), current_user: User = Depends(get_current_user)):
    if current_user.role == "admin":
        return db.query(TestHistory).all()
    return get_user_test_history(db, current_user)


# ✅ 2. Boshqa user test tarixini admin ko‘rsa bo‘ladi
@test_history_router.get("/test_history/{user_id}", response_model=list[TestHistoryOut])
def route_test_history_by_user(user_id: int, db: Session = Depends(database), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Faqat adminlar ko‘rishi mumkin.")
    return get_test_history_by_user(user_id, db)


# ✅ 3. Eng yaxshi o‘quvchilar
@test_history_router.get("/top_students", response_model=list[TopStudentOut])
def route_top_students(db: Session = Depends(database), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Faqat adminlar ko‘rishi mumkin.")
    return get_top_students(db)


# ✅ 4. Test tarixini o‘chirish
@test_history_router.delete("/delete_history/{ident}")
def route_delete_test_history(ident: int, db: Session = Depends(database), current_user: User = Depends(get_current_user)):
    return delete_test_history(ident, db, current_user)
