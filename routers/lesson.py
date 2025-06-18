from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from db import database
from functions.lesson import update_lesson, delete_lesson, create_lesson
from models import Lesson
from routers.auth import get_current_user
from schemas.lessons import CreateLessons, UpdateLessons
from schemas.users import CreateUser

lesson_router = APIRouter(tags=["Lesson"])

@lesson_router.get("/get_lesson")
def get_lesson(db: Lesson = Depends(database)):
    lesson = db.query(Lesson).options(joinedload(Lesson.section_id)).all()
    return lesson



@lesson_router.post("/create_lesson")
def add_lesson(form: CreateLessons, db: Session = Depends(database),
               current_user: CreateUser = Depends(get_current_user)):
    return create_lesson(form, db, current_user)




@lesson_router.put("/update_lesson")
def edit_lesson(ident: int, form: UpdateLessons, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_user)):
    return update_lesson(ident, form, db, current_user)


@lesson_router.delete("/delete_lesson")
def remove_lesson(ident: int, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_user)):
    return delete_lesson(ident, db, current_user)