import os
import shutil
from datetime import datetime
import pytz
from fastapi import HTTPException, UploadFile
from models.lesson import Lesson
from utils.save_file import save_file


def create_lesson(form, db, current_user):
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
    return {"message": "Lesson created successfully", "lesson_id": new_lesson.id}



def update_lesson(ident, form, db, current_user):
    lesson = db.query(Lesson).filter_by(id=ident, created_by=current_user.id).first()
    if not lesson:
        raise HTTPException(403, "Sizga bu darsni tahrirlashga ruxsat yo‘q")
    lesson.title = form.title
    lesson.video_url = form.video_url
    lesson.homework_file_url = form.homework_file_url
    lesson.order = form.order
    lesson.section_id = form.section_id
    db.commit()
    db.refresh(lesson)
    return {"message": "Lesson updated successfully"}



def delete_lesson(ident, db, current_user):
    lesson = db.query(Lesson).filter_by(id=ident, created_by=current_user.id).first()
    if not lesson:
        raise HTTPException(403, "Sizga bu darsni o‘chirishga ruxsat yo‘q")
    db.delete(lesson)
    db.commit()
    return {"message": "Lesson o‘chirildi"}



def upload_homework_file_url(ident, file: UploadFile, db, current_user):
    if current_user.role != 'teacher':
        raise HTTPException(status_code=403, detail="Faqat teacher fayl yuklashi mumkin.")

    lesson = db.query(Lesson).filter(Lesson.id == ident, Lesson.created_by == current_user.id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Sizga tegishli bunday lesson topilmadi.")

    lesson.homework_file_url = save_file(file)
    db.commit()
    return {"message": "Homework file muvaffaqiyatli yuklandi", "file_url": lesson.homework_file_url}


def upload_lesson_video(lesson_id: int, video: UploadFile, db, current_user):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Faqat teacher video yuklashi mumkin.")

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id, Lesson.created_by == current_user.id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Sizga tegishli bunday lesson topilmadi.")

    upload_dir = "static/uploads"
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{datetime.now(pytz.timezone('Asia/Tashkent')).timestamp()}_{video.filename}"
    filepath = os.path.join(upload_dir, filename)

    with open(filepath, "wb") as f:
        shutil.copyfileobj(video.file, f)

    lesson.video_url = f"/static/uploads/{filename}"
    db.commit()
    db.refresh(lesson)

    return {"message": "Video muvaffaqiyatli yuklandi", "video_url": lesson.video_url}
