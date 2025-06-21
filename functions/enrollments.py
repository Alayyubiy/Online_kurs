import pytz
from fastapi import HTTPException
from models.enrollment import Enrollment
from datetime import datetime
from models.payments import Payment

def enroll_user(form, db, current_user):
    if current_user.role != 'admin' and current_user.role != 'teacher':
        raise HTTPException(status_code=403, detail="Sizda kursga yozish huquqi yo‘q.")

    # To‘lov qilinganini tekshirish
    payment = db.query(Payment).filter_by(user_id=form.user_id, course_id=form.course_id, status="paid").first()
    if not payment:
        raise HTTPException(status_code=403, detail="Foydalanuvchi bu kurs uchun to‘lov qilmagan.")

    existing = db.query(Enrollment).filter_by(user_id=form.user_id, course_id=form.course_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu foydalanuvchi allaqachon kursga yozilgan.")

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
    if current_user.role == 'admin':
        return db.query(Enrollment).all()

    elif current_user.role == 'teacher':
        return db.query(Enrollment).join(Enrollment.course).filter(
            Enrollment.course.has(created_by=current_user.id)
        ).all()

    else:
        raise HTTPException(status_code=403, detail="Sizga ruxsat yo‘q.")


def update_enrollment(ident, form, db, current_user):
    enrollment = db.query(Enrollment).filter(Enrollment.id == ident).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Bunday enrollment topilmadi.")

    # teacher o‘z kurslariga tegishli enrollmentni yangilay oladi
    if current_user.role == 'teacher':
        from models.course import Course
        course = db.query(Course).filter(Course.id == enrollment.course_id,
                                         Course.created_by == current_user.id).first()
        if not course:
            raise HTTPException(status_code=403, detail="Siz bu enrollmentni tahrirlashga haqli emassiz.")

    elif current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Sizga ruxsat yo‘q.")

    enrollment.user_id = form.user_id
    enrollment.course_id = form.course_id
    db.commit()
    db.refresh(enrollment)

    return {
        "message": "Enrollment muvaffaqiyatli yangilandi.",
        "data": enrollment
    }


def delete_enrollment(ident, db, current_user):
    enrollment = db.query(Enrollment).filter(Enrollment.id == ident).first()
    if not enrollment:
        raise HTTPException(status_code=404, detail="Bunday enrollment topilmadi.")

    if current_user.role == 'teacher':
        from models.course import Course
        course = db.query(Course).filter(Course.id == enrollment.course_id, Course.created_by == current_user.id).first()
        if not course:
            raise HTTPException(status_code=403, detail="Siz bu enrollmentni o‘chira olmaysiz.")

    elif current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Sizga ruxsat yo‘q.")

    db.delete(enrollment)
    db.commit()

    return {"message": "Enrollment o‘chirildi."}
