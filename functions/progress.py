import pytz
from fastapi import HTTPException

from models import Lesson
from models.progress import Progress
from datetime import datetime
from sqlalchemy.orm import Session


def create_progress(form, db: Session, current_user):
    if current_user.role not in ['admin', 'teacher']:
        raise HTTPException(status_code=403, detail="Sizda progress yozish huquqi yo‘q.")

    existing = db.query(Progress).filter_by(user_id=form.user_id, lesson_id=form.lesson_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu progress allaqachon mavjud")

    # Teacher faqat o‘z darslariga progress yaratishi kerak
    lesson = db.query(Lesson).filter_by(id=form.lesson_id).first()
    if current_user.role == "teacher" and lesson.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Siz faqat o‘zingiz yaratgan darslarga progress qo‘sha olasiz.")

    new_progress = Progress(
        user_id=form.user_id,
        lesson_id=form.lesson_id,
        completed=form.completed,
        completed_at=datetime.now(pytz.timezone("Asia/Tashkent")) if form.completed else None
    )

    db.add(new_progress)
    db.commit()
    db.refresh(new_progress)
    return {"message": "Progress saqlandi", "data": new_progress}



def update_progress(ident: int, form, db: Session, current_user):
    progress = db.query(Progress).filter_by(id=ident).first()
    if not progress:
        raise HTTPException(404, "Bunday progress mavjud emas")

    if current_user.role == "teacher":
        lesson = db.query(Lesson).filter_by(id=progress.lesson_id).first()
        if not lesson or lesson.created_by != current_user.id:
            raise HTTPException(403, "Siz bu progressni yangilay olmaysiz")

    elif current_user.role != "admin":
        raise HTTPException(403, "Sizda huquq yo‘q")

    progress.user_id = form.user_id
    progress.lesson_id = form.lesson_id
    progress.completed = form.completed
    progress.completed_at = datetime.now(pytz.timezone("Asia/Tashkent")) if form.completed else None

    db.commit()
    db.refresh(progress)
    return {"message": "Progress yangilandi", "data": progress}



def get_all_progress(db: Session, current_user):
    if current_user.role == "admin":
        progresses = db.query(Progress).all()
    elif current_user.role == "teacher":
        progresses = db.query(Progress).join(Lesson).filter(Lesson.created_by == current_user.id).all()
    else:
        raise HTTPException(403, "Sizda progresslarni ko‘rish huquqi yo‘q")

    return [
        {
            "id": p.id,
            "user_id": p.user_id,
            "lesson_id": p.lesson_id,
            "completed": p.completed,
            "completed_at": str(p.completed_at) if p.completed_at else None
        }
        for p in progresses
    ]
def delete_progress(ident: int, db: Session, current_user):
    progress = db.query(Progress).filter(Progress.id == ident).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Progress topilmadi.")

    # Teacher o‘ziga tegishli lesson orqali yaratilgan progressni o‘chira oladi
    if current_user.role == "teacher":
        lesson = db.query(Lesson).filter_by(id=progress.lesson_id).first()
        if not lesson or lesson.created_by != current_user.id:
            raise HTTPException(status_code=403, detail="Siz bu progressni o‘chira olmaysiz.")

    elif current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Sizda progressni o‘chirishga ruxsat yo‘q.")

    db.delete(progress)
    db.commit()

    return {"message": "Progress muvaffaqiyatli o‘chirildi."}

