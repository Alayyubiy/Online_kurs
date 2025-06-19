import os
import shutil
from datetime import datetime
import pytz
from fastapi import HTTPException, UploadFile
from models.lesson import Lesson
from utils.save_file import save_file


def create_lesson(form, db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(403, detail="Sizga bu amalni bajarishga ruxsat yo'q")

    new_lesson = Lesson(
        title=form.title.strip(),
        order=form.order,
        section_id=form.section_id
    )
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return {"message": "Lesson created successfully", "lesson_id": new_lesson.id}



def update_lesson(ident, form, db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(403, detail="Faqat admin yangilashi mumkin")
    lesson = db.query(Lesson).filter(Lesson.id == ident).first()
    if not lesson:
        raise HTTPException(404, detail="Lesson topilmadi")
    for key, value in form.dict(exclude_unset=True).items():
        setattr(lesson, key, value)
    db.commit()
    return {"message": "Lesson updated successfully"}



def delete_lesson(ident, db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(403, detail="Faqat admin o'chirishi mumkin")

    lesson = db.query(Lesson).filter(Lesson.id == ident).first()
    if not lesson:
        raise HTTPException(404, detail="Lesson mavjud emas")

    db.delete(lesson)
    db.commit()
    return {"message": "Lesson deleted successfully"}


def upload_homework_file_url(ident,image,db,current_user):
    if current_user.role == 'admin':
        lesson = db.query(Lesson).filter(Lesson.id == ident).first()
        if not lesson:
            raise HTTPException(404, "The apartment you entered does not exist!!!")

        lesson.image = save_file(image)
        db.commit()
        return {"message": "Image downloads"}
    else:
        return {"Message": "Sizda adminlik huquqi mavjud emas !!!"}



def upload_lesson_video(lesson_id: int, video: UploadFile, db, current_user):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Faqat adminlar video yuklashi mumkin.")

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Bunday dars topilmadi.")

    upload_dir = "static/uploads"
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{datetime.now(pytz.timezone("Asia/Tashkent")).timestamp()}_{video.filename}"
    filepath = os.path.join(upload_dir, filename)

    with open(filepath, "wb") as f:
        shutil.copyfileobj(video.file, f)

    lesson.video_url = f"/static/uploads/{filename}"
    db.commit()
    db.refresh(lesson)

    return {"message": "Video muvaffaqiyatli yuklandi", "video_url": lesson.video_url}
