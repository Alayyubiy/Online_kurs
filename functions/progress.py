import pytz
from fastapi import HTTPException
from models.progress import Progress
from datetime import datetime


def create_progress(form, db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Faqat adminlar ruxsat etiladi.")
    old = db.query(Progress).filter_by(user_id=form.user_id, lesson_id=form.lesson_id).first()
    if old:
        raise HTTPException(status_code=400, detail="Bu progress allaqachon mavjud")

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


def update_progress(ident, form, db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Faqat admin foydalanuvchilar progressni yangilashi mumkin!")

    progress = db.query(Progress).filter(Progress.id == ident).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Bunday progress mavjud emas!")

    progress.user_id = form.user_id
    progress.lesson_id = form.lesson_id
    progress.completed = form.completed
    progress.completed_at = form.completed_at or datetime.now(pytz.timezone("Asia/Tashkent"))

    db.commit()
    db.refresh(progress)
    return {"message": "Progress muvaffaqiyatli yangilandi!", "data": {
        "id": progress.id,
        "user_id": progress.user_id,
        "lesson_id": progress.lesson_id,
        "completed": progress.completed,
        "completed_at": progress.completed_at
    }}



def get_all_progress(db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Faqat adminlar ko‘rishi mumkin")
    return db.query(Progress).all()
