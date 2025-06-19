import pytz
from fastapi import HTTPException
from models.progress import Progress
from datetime import datetime
from sqlalchemy.orm import Session


def create_progress(form, db: Session, current_user):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Faqat adminlar ruxsat etiladi.")


    existing = db.query(Progress).filter_by(user_id=form.user_id, lesson_id=form.lesson_id).first()
    if existing:
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

    return {
        "message": "Progress saqlandi",
        "data": {
            "id": new_progress.id,
            "user_id": new_progress.user_id,
            "lesson_id": new_progress.lesson_id,
            "completed": new_progress.completed,
            "completed_at": str(new_progress.completed_at) if new_progress.completed_at else None
        }
    }


def update_progress(ident: int, form, db: Session, current_user):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=403,
            detail="Faqat admin foydalanuvchilar progressni yangilashi mumkin!"
        )

    progress = db.query(Progress).filter(Progress.id == ident).first()
    if not progress:
        raise HTTPException(
            status_code=404,
            detail="Bunday progress mavjud emas!"
        )

    progress.user_id = form.user_id
    progress.lesson_id = form.lesson_id
    progress.completed = form.completed

    if form.completed:
        progress.completed_at = form.completed_at or datetime.now(pytz.timezone("Asia/Tashkent"))
    else:
        progress.completed_at = None

    db.commit()
    db.refresh(progress)

    return {
        "message": "Progress muvaffaqiyatli yangilandi!",
        "data": {
            "id": progress.id,
            "user_id": progress.user_id,
            "lesson_id": progress.lesson_id,
            "completed": progress.completed,
            "completed_at": str(progress.completed_at) if progress.completed_at else None
        }
    }


def get_all_progress(db: Session, current_user):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Faqat adminlar ko‘rishi mumkin")

    progresses = db.query(Progress).all()

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
