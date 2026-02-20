from typing import Optional
import pytz
from models.payments import Payment
from datetime import datetime
from sqlalchemy.orm import Session
from models import   User, Course
from fastapi import HTTPException


# 1. To‘lov qilganlar ro‘yxati
def get_paid_users(course_id: int, db: Session):
    results = (
        db.query(
            User.name.label("name"),
            User.phone.label("phone"),
            Course.name.label("course_name"),
            Payment.paid_at.label("paid_at")
        )
        .join(Payment, Payment.user_id == User.id)
        .join(Course, Course.id == Payment.course_id)
        .filter(Payment.course_id == course_id, Payment.status == "paid")
        .all()
    )

    return [
        {
            "name": row.name,
            "phone": row.phone,
            "course_name": row.course_name,
            "paid_at": row.paid_at.strftime('%Y-%m-%d %H:%M') if row.paid_at else None
        }
        for row in results
    ]


# 2. To‘lov qilmaganlar ro‘yxati
def get_unpaid_enrollments(course_id: int, db: Session):
    subquery = (
        db.query(Payment.user_id)
        .filter(Payment.course_id == course_id, Payment.status == "paid")
        .subquery()
    )
    # Enrollment o'rniga barcha userlarni Payment jadvalidan oling
    results = (
        db.query(User.name, User.phone, Course.name.label("course_name"))
        .join(Payment, Payment.user_id == User.id)
        .join(Course, Course.id == Payment.course_id)
        .filter(Payment.course_id == course_id)
        .filter(~User.id.in_(subquery))
        .all()
    )

    return [
        {
            "name": row.name,
            "phone": row.phone,
            "course_name": row.course_name,
            "paid_at": None  # to‘lov qilmagan
        }
        for row in results
    ]

def add_manual_payment(user_id: int, course_id: int, db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Faqat admin to‘lov qo‘sha oladi.")

    user = db.query(User).filter(User.id == user_id).first()
    course = db.query(Course).filter(Course.id == course_id).first()

    if not user or not course:
        raise HTTPException(status_code=404, detail="Foydalanuvchi yoki kurs topilmadi.")

    old_payment = db.query(Payment).filter_by(user_id=user_id, course_id=course_id).first()
    if old_payment:
        raise HTTPException(status_code=400, detail="Bu foydalanuvchi allaqachon bu kurs uchun to‘lov qilgan.")

    new_payment = Payment(
        user_id=user_id,
        course_id=course_id,
        amount=course.price,
        status="paid",
        paid_at=datetime.now(pytz.timezone("Asia/Tashkent"))
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return {
        "message": "To‘lov muvaffaqiyatli qo‘shildi.",
        "payment_id": new_payment.id
    }

def update_payment_status(payment_id: int, new_status: Optional[str], new_amount: Optional[float], db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Faqat admin o‘zgartira oladi.")

    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="To‘lov topilmadi.")

    if new_status:
        if new_status not in ["pending", "paid", "unpaid"]:
            raise HTTPException(status_code=400, detail="Noto‘g‘ri status.")
        payment.status = new_status

        if new_status == "paid" and not payment.paid_at:
            payment.paid_at = datetime.now(pytz.timezone("Asia/Tashkent"))

    if new_amount is not None:
        if new_amount < 0:
            raise HTTPException(status_code=400, detail="To‘lov miqdori manfiy bo‘lishi mumkin emas.")
        payment.amount = new_amount

    db.commit()
    db.refresh(payment)

    return {
        "message": "To‘lov muvaffaqiyatli yangilandi.",
        "payment_id": payment.id,
        "status": payment.status,
        "amount": payment.amount,
        "paid_at": payment.paid_at.strftime('%Y-%m-%d %H:%M') if payment.paid_at else None
    }


