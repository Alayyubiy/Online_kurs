from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import database
from models.quiz import Quiz
from routers.auth import get_current_user
from models.user import User
from schemas.quiz import CreateQuiz, QuizAnswer
from functions.quiz import create_quiz, submit_quiz, update_quiz, delete_quiz

quiz_router = APIRouter(tags=["Quiz"])


@quiz_router.get("/get_quizzes/{lesson_id}")
def route_get_quizzes(lesson_id: int,
                      db: Session = Depends(database),
                      current_user: User = Depends(get_current_user)):  # models.users.Users bo‘lishi kerak!
    if not current_user:
        raise HTTPException(status_code=401, detail="Avval login qiling.")

    return db.query(Quiz).filter(Quiz.lesson_id == lesson_id).all()


@quiz_router.post("/add_quiz")
def route_add_quiz(form: CreateQuiz, db: Session = Depends(database),
                   current_user: User = Depends(get_current_user)):
    return create_quiz(form, db, current_user)


@quiz_router.post("/submit_quiz/{lesson_id}")
def route_submit_quiz(lesson_id: int, form: QuizAnswer, db: Session = Depends(database),
                      current_user: User = Depends(get_current_user)):
    return submit_quiz(lesson_id, current_user.id, form.answers, db)


@quiz_router.put("/update_quiz/{quiz_id}")
def route_update_quiz(quiz_id: int,
                      form: CreateQuiz,
                      db: Session = Depends(database),
                      current_user: User = Depends(get_current_user)):
    return update_quiz(quiz_id, form, db, current_user)


@quiz_router.delete("/delete_quiz/{quiz_id}")
def route_delete_quiz(quiz_id: int,
                      db: Session = Depends(database),
                      current_user: User = Depends(get_current_user)):
    return delete_quiz(quiz_id, db, current_user)
