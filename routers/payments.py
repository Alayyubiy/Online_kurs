from datetime import datetime

import pytz
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from models import User, Course
from models.payments import Payment
from functions.payments import get_unpaid_enrollments, get_paid_users, add_manual_payment, update_payment_status
from db import database
from routers.auth import get_current_user

payment_router = APIRouter(tags=["Payment"])


# ✅ FIX 1: Frontend /create-payment endpointini qo'shish
@payment_router.post("/create-payment")
def create_payment(
    data: dict = Body(...),
    db: Session = Depends(database),
    current_user: User = Depends(get_current_user)
):
    course_id = data.get("course_id")
    if not course_id:
        raise HTTPException(status_code=400, detail="course_id kiritilmadi")

    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs topilmadi")

    # Ikki marta to'lamaslik
    existing = db.query(Payment).filter_by(
        user_id=current_user.id, course_id=course_id
    ).first()
    if existing and existing.status == "paid":
        raise HTTPException(status_code=400, detail="Siz bu kursni allaqachon sotib olgansiz")

    payment = Payment(
        user_id=current_user.id,
        course_id=course_id,
        amount=course.price,
        status="paid",
        paid_at=datetime.now(pytz.timezone("Asia/Tashkent"))
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return {"message": "To'lov muvaffaqiyatli qabul qilindi", "payment_id": payment.id}


# ✅ FIX 2: Frontend /check-access/{courseId} endpointini qo'shish
@payment_router.get("/check-access/{course_id}")
def check_access(
    course_id: int,
    db: Session = Depends(database),
    current_user: User = Depends(get_current_user)
):
    # Bepul kurs
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Kurs topilmadi")

    if course.price == 0:
        return {"has_access": True}

    payment = db.query(Payment).filter_by(
        user_id=current_user.id,
        course_id=course_id,
        status="paid"
    ).first()
    return {"has_access": bool(payment)}


# ✅ FIX 3: Frontend /my-payments endpointini qo'shish
@payment_router.get("/my-payments")
def my_payments(
    db: Session = Depends(database),
    current_user: User = Depends(get_current_user)
):
    payments = db.query(Payment).filter_by(
        user_id=current_user.id,
        status="paid"
    ).all()
    return [
        {
            "id": p.id,
            "course_id": p.course_id,
            "amount": p.amount,
            "status": p.status,
            "paid_at": p.paid_at.strftime('%Y-%m-%d %H:%M') if p.paid_at else None
        }
        for p in payments
    ]


# --- Mavjud endpointlar ---

@payment_router.get("/paid-users/{course_id}")
def paid_users(
    course_id: int,
    db: Session = Depends(database),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Faqat admin ko'ra oladi")
    return get_paid_users(course_id, db)


@payment_router.get("/unpaid-users/{course_id}")
def unpaid_users(
    course_id: int,
    db: Session = Depends(database),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Faqat admin ko'ra oladi")
    return get_unpaid_enrollments(course_id, db)


@payment_router.post("/manual-payment")
def manual_payment(
    user_id: int = Body(...),
    course_id: int = Body(...),
    db: Session = Depends(database),
    current_user: User = Depends(get_current_user)
):
    return add_manual_payment(user_id, course_id, db, current_user)


class UpdatePaymentStatus(BaseModel):
    payment_id: int
    new_status: Optional[str] = None
    new_amount: Optional[float] = None


@payment_router.put("/update-status")
def route_update_payment_status(
    data: UpdatePaymentStatus,
    db: Session = Depends(database),
    current_user: User = Depends(get_current_user)
):
    return update_payment_status(data.payment_id, data.new_status, data.new_amount, db, current_user)