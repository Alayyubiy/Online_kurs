import pytz
from fastapi import HTTPException
from models.enrollment import Enrollment
from datetime import datetime



def enroll_user(form, db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Faqat adminlar foydalanuvchilarni kursga yozishi mumkin.")
    existing = db.query(Enrollment).filter_by(user_id=form.user_id, course_id=form.course_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu foydalanuvchi allaqachon bu kursga yozilgan.")

    new_enrollment = Enrollment(
        user_id=form.user_id,
        course_id=form.course_id,
        enrolled_at=datetime.now(pytz.timezone("Asia/Tashkent"))
    )
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return {
        "message": "Foydalanuvchi kursga yozildi.",
        "data": new_enrollment
    }



def get_all_enrollments(db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Faqat adminlar ro'yxatni ko'rishi mumkin.")

    return db.query(Enrollment).all()



def update_enrollment(ident, form, db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Faqat admin foydalanuvchilarni yangilay oladi.")

    enrollment = db.query(Enrollment).filter(Enrollment.id == ident).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Bunday enrollment mavjud emas.")

    enrollment.user_id = form.user_id
    enrollment.course_id = form.course_id
    db.commit()
    db.refresh(enrollment)

    return {
        "message": "Enrollment muvaffaqiyatli yangilandi.",
        "data": enrollment
    }



def delete_enrollment(ident, db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Faqat adminlar o‘chira oladi.")

    enrollment = db.query(Enrollment).filter(Enrollment.id == ident).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Bunday enrollment topilmadi.")

    db.delete(enrollment)
    db.commit()

    return {"message": "Enrollment o‘chirildi."}