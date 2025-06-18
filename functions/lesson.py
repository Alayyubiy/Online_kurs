from fastapi import HTTPException
from models.lesson import Lesson

def create_lesson(form, db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(403, detail="Sizga bu amalni bajarishga ruxsat yo'q")

    new_lesson = Lesson(
        title=form.title.strip(),
        video_url=form.video_url,
        homework_file_url=form.homework_file_url,
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
