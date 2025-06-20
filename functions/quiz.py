from fastapi import HTTPException
from models import Lesson
from models.quiz import Quiz
from models.progress import Progress
from datetime import datetime
import pytz

def create_quiz(form, db, current_user):
    # Dars mavjudligini tekshirish
    lesson = db.query(Lesson).filter(Lesson.id == form.lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Bunday dars topilmadi!")

    # Ruxsatni tekshirish: admin hamma narsani, teacher faqat o‘zinikini
    if current_user.role == "teacher" and lesson.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Faqat o‘zingizga tegishli darsga quiz qo‘shishingiz mumkin!")

    # Quiz qo‘shish
    quiz = Quiz(
        lesson_id=form.lesson_id,
        question=form.question,
        correct_answer=form.correct_answer
    )
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return {"message": "Quiz muvaffaqiyatli qo‘shildi", "quiz_id": quiz.id}

def update_quiz(quiz_id, form, db, current_user):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz topilmadi!")

    # Lesson bilan bog'liq tekshirish
    lesson = db.query(Lesson).filter(Lesson.id == quiz.lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Bog‘langan dars topilmadi!")

    # Ruxsat nazorati
    if current_user.role == "teacher" and lesson.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Faqat o‘z quizlaringizni o‘zgartirishingiz mumkin!")

    quiz.question = form.question
    quiz.correct_answer = form.correct_answer
    db.commit()
    db.refresh(quiz)

    return {"message": "Quiz muvaffaqiyatli yangilandi", "quiz_id": quiz.id}


def delete_quiz(quiz_id, db, current_user):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz topilmadi!")

    lesson = db.query(Lesson).filter(Lesson.id == quiz.lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Bog‘langan dars topilmadi!")

    if current_user.role == "teacher" and lesson.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Faqat o‘z quizlaringizni o‘chira olasiz!")

    db.delete(quiz)
    db.commit()
    return {"message": "Quiz o‘chirildi"}


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
