from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import User
from functions.payments import get_unpaid_enrollments, get_paid_users, add_manual_payment, update_payment_status
from db import database
from routers.auth import get_current_user

payment_router = APIRouter(tags=["Payment"])

@payment_router.get("/paid-users/{course_id}")
def paid_users(course_id: int, db: Session = Depends(database), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Faqat admin ko‘ra oladi")
    return get_paid_users(course_id, db)


@payment_router.get("/unpaid-users/{course_id}")
def unpaid_users(course_id: int, db: Session = Depends(database), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Faqat admin ko‘ra oladi")
    return get_unpaid_enrollments(course_id, db)

from fastapi import Body

@payment_router.post("/manual-payment")
def manual_payment(
    user_id: int = Body(...),
    course_id: int = Body(...),
    db: Session = Depends(database),
    current_user: User = Depends(get_current_user)
):
    return add_manual_payment(user_id, course_id, db, current_user)


from pydantic import BaseModel

class UpdatePaymentStatus(BaseModel):
    payment_id: int
    new_status: str  # "paid", "pending", "failed"

@payment_router.put("/update-status")
def route_update_payment_status(
    data: UpdatePaymentStatus,
    db: Session = Depends(database),
    current_user: User = Depends(get_current_user)
):
    return update_payment_status(data.payment_id, data.new_status, db, current_user)
