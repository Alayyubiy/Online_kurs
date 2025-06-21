from fastapi import HTTPException

from models import User
from models.live_sessions import LiveSession
from models.course import Course
from sqlalchemy.orm import Session


def get_student_live_sessions(db: Session, current_user):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Faqat studentlar ko‘rishi mumkin")

    from models import Enrollment
    return db.query(LiveSession).join(Enrollment, Enrollment.course_id == LiveSession.course_id) \
        .filter(Enrollment.user_id == current_user.id).all()


def get_all_live_sessions(db: Session, current_user):
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Faqat admin yoki ustoz ko‘rishi mumkin")

    if current_user.role == "teacher":
        from models.course import Course
        teacher_courses = db.query(Course.id).filter(Course.created_by == current_user.id).subquery()
        return db.query(LiveSession).filter(LiveSession.course_id.in_(teacher_courses)).all()

    return db.query(LiveSession).all()

def create_live_session(form, db: Session, current_user):
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Sizda bu amal uchun ruxsat yo'q.")


    if current_user.role == "teacher":
        course = db.query(Course).filter(Course.id == form.course_id, Course.created_by == current_user.id).first()
        if not course:
            raise HTTPException(status_code=403, detail="Bu kurs sizga tegishli emas.")
    course = db.query(Course).filter(Course.id == form.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Bunday kurs topilmadi")
    live = LiveSession(
        title=form.title,
        course_id=form.course_id,
        host_id=current_user.id,
        start_time=form.start_time,
        room_link=form.room_link
    )
    db.add(live)
    db.commit()
    db.refresh(live)

    return {"message": "Live session yaratildi!", "room_link": live.room_link}





def update_live_session(ident: int, form, db: Session, current_user):
    # Foydalanuvchini roli tekshiriladi
    if current_user.role not in ['admin', 'teacher']:
        raise HTTPException(status_code=403, detail="Sizda ruxsat yo'q!")

    # Mavjud sessiyani topamiz
    session = db.query(LiveSession).filter(LiveSession.id == ident).first()
    if not session:
        raise HTTPException(status_code=404, detail="Bunday live sessiya topilmadi")

    # Agar teacher bo‘lsa, faqat o‘zi yaratgan sessiyani yangilay oladi
    if current_user.role == 'teacher' and session.host_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu sessiyani o‘zgartirishga huquqingiz yo‘q")

    # Kurs mavjudligini tekshirish
    course = db.query(Course).filter(Course.id == form.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Bunday kurs mavjud emas")

    # Yangilash
    session.title = form.title.strip()
    session.course_id = form.course_id
    session.start_time = form.start_time
    session.room_link = form.room_link.strip()

    db.commit()
    db.refresh(session)

    return {"message": "Sessiya muvaffaqiyatli yangilandi", "data": session}



def delete_live_session(session_id: int, db: Session, current_user: User):
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Sizda ruxsat yo‘q")

    live_session = db.query(LiveSession).filter(LiveSession.id == session_id).first()
    if not live_session:
        raise HTTPException(status_code=404, detail="Jonli sessiya topilmadi")

    # Teacher faqat o‘zini sessiyasini o‘chira oladi
    if current_user.role == "teacher" and live_session.host_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu sessiyani o‘chirishga ruxsatingiz yo‘q")

    db.delete(live_session)
    db.commit()
    return {"message": "Jonli sessiya muvaffaqiyatli o‘chirildi"}