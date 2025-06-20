import os
import shutil
from datetime import datetime
import pytz
from fastapi import HTTPException, UploadFile
from models.lesson import Lesson
from utils.save_file import save_file


def create_lesson(form, db, current_user):
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Faqat admin yoki teacher lesson yaratishi mumkin.")

    new_lesson = Lesson(
        title=form.title,
        video_url=form.video_url,
        homework_file_url=form.homework_file_url,
        order=form.order,
        section_id=form.section_id,
        created_by=current_user.id
    )
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return {"message": "Lesson yaratildi", "lesson_id": new_lesson.id}


def update_lesson(ident, form, db, current_user):
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Ruxsatingiz yo‘q.")

    query = db.query(Lesson).filter(Lesson.id == ident)
    if current_user.role == "teacher":
        query = query.filter(Lesson.created_by == current_user.id)

    lesson = query.first()
    if not lesson:
        raise HTTPException(404, "Lesson topilmadi yoki sizga tegishli emas.")

    lesson.title = form.title
    lesson.video_url = form.video_url
    lesson.homework_file_url = form.homework_file_url
    lesson.order = form.order
    lesson.section_id = form.section_id
    db.commit()
    db.refresh(lesson)
    return {"message": "Lesson muvaffaqiyatli yangilandi"}


def delete_lesson(ident, db, current_user):
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Sizda o‘chirish huquqi yo‘q.")

    query = db.query(Lesson).filter(Lesson.id == ident)
    if current_user.role == "teacher":
        query = query.filter(Lesson.created_by == current_user.id)

    lesson = query.first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson topilmadi yoki sizga tegishli emas.")

    db.delete(lesson)
    db.commit()
    return {"message": "Lesson o‘chirildi"}


def upload_homework_file_url(ident, file: UploadFile, db, current_user):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Faqat teacher fayl yuklashi mumkin.")

    lesson = db.query(Lesson).filter(Lesson.id == ident, Lesson.created_by == current_user.id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson topilmadi yoki sizga tegishli emas.")

    lesson.homework_file_url = save_file(file)
    db.commit()
    return {"message": "Homework yuklandi", "file_url": lesson.homework_file_url}


def upload_lesson_video(lesson_id: int, video: UploadFile, db, current_user):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Faqat teacher video yuklashi mumkin.")

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id, Lesson.created_by == current_user.id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson topilmadi yoki sizga tegishli emas.")

    upload_dir = "static/uploads"
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{datetime.now(pytz.timezone('Asia/Tashkent')).timestamp()}_{video.filename}"
    filepath = os.path.join(upload_dir, filename)

    with open(filepath, "wb") as f:
        shutil.copyfileobj(video.file, f)

    lesson.video_url = f"/static/uploads/{filename}"
    db.commit()
    db.refresh(lesson)

    return {"message": "Video yuklandi", "video_url": lesson.video_url}
