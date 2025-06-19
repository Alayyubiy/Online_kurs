from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session, joinedload
from db import database
from functions.lesson import update_lesson, delete_lesson, create_lesson, upload_homework_file_url, upload_lesson_video
from models import Lesson, User
from routers.auth import get_current_user
from schemas.lessons import CreateLessons, UpdateLessons
from schemas.users import CreateUser

lesson_router = APIRouter(tags=["Lesson"])


@lesson_router.get("/get_lesson")
def get_lesson(db: Lesson = Depends(database)):
    lesson = db.query(Lesson).options(joinedload(Lesson.section)).all()
    return lesson



@lesson_router.post("/create_lesson")
def add_lesson(form: CreateLessons, db: Session = Depends(database),
               current_user: CreateUser = Depends(get_current_user)):
    return create_lesson(form, db, current_user)


@lesson_router.post("/upload_video/{lesson_id}")
def route_upload_video(
    lesson_id: int,
    video: UploadFile = File(...),
    db: Session = Depends(database),
    current_user: User = Depends(get_current_user)
):
    return upload_lesson_video(lesson_id, video, db, current_user)

@lesson_router.post('/create_image')
def lesson_image(ident: int, file: UploadFile,db:Session = Depends(database),
                    current_user: CreateUser = Depends(get_current_user)):
    return upload_homework_file_url(ident,file,db,current_user)


@lesson_router.put("/update_lesson")
def edit_lesson(ident: int, form: UpdateLessons, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_user)):
    return update_lesson(ident, form, db, current_user)



@lesson_router.delete("/delete_lesson")
def remove_lesson(ident: int, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_user)):
    return delete_lesson(ident, db, current_user)