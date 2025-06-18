from typing import Optional, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from functions.courses import create_courses,update_courses,delete_courses
from models.course import Course
from routers.auth import get_current_user
from schemas.users import CreateUser
from schemas.courses import CreateCourses,UpdateCourses,CourseOut
from db import database


courses_router = APIRouter(tags=["Course"])


@courses_router.get("/get_courses")
def get_courses(name: Optional[str] = None, db: Session = Depends(database)):
    query = db.query(Course).options(joinedload(Course.sections))
    if name:
        query = query.filter(Course.name == name)

    return query.all()



@courses_router.post('/create_apartment')
def create_course(form:CreateCourses,db:Session = Depends(database),
                      current_user: CreateUser = Depends(get_current_user)):
    return create_courses(form,db,current_user)


@courses_router.put('/update_apartment')
def update_course(ident : int,form:UpdateCourses,db:Session = Depends(database),
                      current_user: CreateUser = Depends(get_current_user)):
    return update_courses(ident,form,db,current_user)


@courses_router.delete('/delete_apartment')
def delete_course(ident: int,db:Session = Depends(database),
                      current_user: CreateUser = Depends(get_current_user)):
    return delete_courses(ident,db,current_user)
