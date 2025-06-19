from fastapi import HTTPException

from models import Lesson
from models.quiz import Quiz
from models.progress import Progress
from datetime import datetime
import pytz

def create_quiz(form, db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Faqat adminlar test qo‘shishi mumkin.")
    lesson = db.query(Lesson).filter(Lesson.id == form.lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Bunday dars mavjud emas!")
    new_quiz = Quiz(
        lesson_id=form.lesson_id,
        question=form.question.strip(),
        correct_answer=form.correct_answer.strip()
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    return {"message": "Savol qo‘shildi", "id": new_quiz.id}


def submit_quiz(lesson_id, user_id, answers: dict, db):
    quizzes = db.query(Quiz).filter(Quiz.lesson_id == lesson_id).all()
    if not quizzes:
        raise HTTPException(status_code=404, detail="Bu darsga test topilmadi.")

    total = len(quizzes)
    correct = 0

    for quiz in quizzes:
        user_answer = answers.get(quiz.id)
        if user_answer and user_answer.strip().lower() == quiz.correct_answer.strip().lower():
            correct += 1

    score = round((correct / total) * 100, 2)

    progress = db.query(Progress).filter_by(user_id=user_id, lesson_id=lesson_id).first()
    if progress:
        progress.completed = score >= 60
        progress.completed_at = datetime.now(pytz.timezone("Asia/Tashkent")) if score >= 60 else None
    else:
        db.add(Progress(
            user_id=user_id,
            lesson_id=lesson_id,
            completed=score >= 60,
            completed_at=datetime.now(pytz.timezone("Asia/Tashkent")) if score >= 60 else None
        ))

    db.commit()
    return {
        "score": score,
        "status": "✅" if score >= 60 else "❌",
        "message": "Keyingi darsga o'tishingiz mumkin." if score >= 60 else "Iltimos, darsni qayta ko‘rib chiqing."
    }
