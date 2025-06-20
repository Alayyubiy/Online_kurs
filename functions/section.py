from fastapi import HTTPException
from models.section import Section
from models.course import Course
from models.user import User


def create_section(form, db, current_user: User):
    course = db.query(Course).filter(Course.id == form.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course topilmadi.")

    if current_user.role == 'teacher' and course.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Faqat o‘zingiz yaratgan kursga section qo‘sha olasiz.")

    if current_user.role not in ['admin', 'teacher']:
        raise HTTPException(status_code=403, detail="Sizda ruxsat yo‘q.")

    section = Section(
        title=form.title.strip().capitalize(),
        order=form.order,
        course_id=form.course_id
    )
    db.add(section)
    db.commit()
    db.refresh(section)
    return {"message": "Section muvaffaqiyatli yaratildi", "section_id": section.id}


def update_section(ident, form, db, current_user: User):
    section = db.query(Section).filter(Section.id == ident).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section topilmadi.")

    course = db.query(Course).filter(Course.id == section.course_id).first()
    if current_user.role == 'teacher' and course.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Faqat o‘zingiz yaratgan kurs sectionini tahrirlashingiz mumkin.")

    if current_user.role not in ['admin', 'teacher']:
        raise HTTPException(status_code=403, detail="Sizda ruxsat yo‘q.")

    section.title = form.title.strip().capitalize()
    section.order = form.order
    db.commit()
    return {"message": "Section yangilandi"}


def delete_section(ident, db, current_user: User):
    section = db.query(Section).filter(Section.id == ident).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section topilmadi.")

    course = db.query(Course).filter(Course.id == section.course_id).first()
    if current_user.role == 'teacher' and course.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Faqat o‘zingiz yaratgan kurs bo‘limini o‘chira olasiz.")

    if current_user.role not in ['admin', 'teacher']:
        raise HTTPException(status_code=403, detail="Sizda ruxsat yo‘q.")

    db.delete(section)
    db.commit()
    return {"message": "Section o‘chirildi"}
