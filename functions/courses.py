from fastapi import HTTPException
from models.course import Course


def create_courses(form, db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Sizda adminlik huquqi mavjud emas!")

    new_course = Course(
        name=form.name.strip().capitalize(),
        description=form.description.strip(),
        category=form.category.strip(),
        duration=form.duration.strip(),
        level=form.level.strip(),
        price=form.price,
        teacher=form.teacher.strip(),
        lessons=form.lessons,
        views=form.views,
        created_by = current_user.id

    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return  new_course


def update_courses(ident, form, db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Sizda adminlik huquqi mavjud emas!")

    course = db.query(Course).filter(Course.id == ident).first()
    if not course:
        raise HTTPException(status_code=404, detail="Bunday kurs topilmadi!")

    course.name = form.name.strip().capitalize()
    course.description = form.description.strip()

    db.commit()
    db.refresh(course)
    return {"message": "Kurs muvaffaqiyatli yangilandi", "course_id": course.id}


def delete_courses(ident, db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Sizda adminlik huquqi mavjud emas!")

    course = db.query(Course).filter(Course.id == ident).first()
    if not course:
        raise HTTPException(status_code=404, detail="Bunday kurs mavjud emas!")

    db.delete(course)
    db.commit()
    return {"message": "Kurs bazadan muvaffaqiyatli o‘chirildi"}
