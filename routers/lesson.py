from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session, joinedload
from db import database
from functions.lesson import (
    update_lesson, delete_lesson, create_lesson,
    upload_homework_file_url, upload_lesson_video
)
from models import Lesson, User
from routers.auth import get_current_user
from schemas.lessons import CreateLessons, UpdateLessons

lesson_router = APIRouter(tags=["Lesson"])


@lesson_router.get("/get_lesson")
def get_lesson(db: Session = Depends(database), current_user: User = Depends(get_current_user)):
    if current_user.role == "admin":
        lessons = db.query(Lesson).options(joinedload(Lesson.section)).all()
    elif current_user.role == "teacher":
        lessons = db.query(Lesson).filter(Lesson.created_by == current_user.id).options(joinedload(Lesson.section)).all()
    else:
        raise HTTPException(status_code=403, detail="Sizga ruxsat yo‘q.")
    return lessons


@lesson_router.post("/create_lesson")
def add_lesson(form: CreateLessons, db: Session = Depends(database),
               current_user: User = Depends(get_current_user)):
    return create_lesson(form, db, current_user)


@lesson_router.post("/upload_video/{lesson_id}")
def route_upload_video(
    lesson_id: int,
    video: UploadFile = File(...),
    db: Session = Depends(database),
    current_user: User = Depends(get_current_user)
):
    return upload_lesson_video(lesson_id, video, db, current_user)


@lesson_router.post("/upload_homework/{lesson_id}")
def route_upload_homework(
    lesson_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(database),
    current_user: User = Depends(get_current_user)
):
    return upload_homework_file_url(lesson_id, file, db, current_user)


@lesson_router.put("/update_lesson")
def edit_lesson(ident: int, form: UpdateLessons,
                db: Session = Depends(database),
                current_user: User = Depends(get_current_user)):
    return update_lesson(ident, form, db, current_user)


@lesson_router.delete("/delete_lesson")
def remove_lesson(ident: int, db: Session = Depends(database),
                  current_user: User = Depends(get_current_user)):
    return delete_lesson(ident, db, current_user)
