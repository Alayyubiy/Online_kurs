from typing import Optional, List
from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session, joinedload
from functions.courses import update_courses,delete_courses,create_courses
from models.course import Course
from models.course_image import CourseImage
from routers.auth import get_current_user
from schemas.users import CreateUser
from schemas.courses import UpdateCourses, CreateCourses
from db import database
from utils.save_file import save_image

courses_router = APIRouter(tags=["Course"])


@courses_router.get("/get_courses")
def get_courses(name: Optional[str] = None, db: Session = Depends(database)):
    query = db.query(Course).options(joinedload(Course.sections))
    if name:
        query = query.filter(Course.name == name)

    return query.all()



@courses_router.post('/create_course')
def create_course(
    name: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    duration: str = Form(...),
    level: str = Form(...),
    price: int = Form(...),
    teacher: str = Form(...),
    images: List[UploadFile] = File(None),
    db: Session = Depends(database),
    current_user: CreateUser = Depends(get_current_user)
):
    # Kurs yaratish
    form = CreateCourses(
        name=name,
        description=description,
        category=category,
        duration=duration,
        level=level,
        price=price,
        teacher=teacher
    )
    course = create_courses(form, db, current_user)


    # Rasmlar yuklash
    if images:
        for img in images:
            filename = save_image(img)
            new_image = CourseImage(course_id=course.id, image=filename)
            db.add(new_image)
        db.commit()

    return {"msg": "Course created with images", "course_id": course.id}

@courses_router.put('/update_apartment')
def update_course(ident : int,form:UpdateCourses,db:Session = Depends(database),
                      current_user: CreateUser = Depends(get_current_user)):
    return update_courses(ident,form,db,current_user)


@courses_router.delete('/delete_apartment')
def delete_course(ident: int,db:Session = Depends(database),
                      current_user: CreateUser = Depends(get_current_user)):
    return delete_courses(ident,db,current_user)
