# services/statistics.py
from datetime import datetime

import pytz
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.quiz import Quiz
from models.test_history  import TestHistory


def get_user_scores_chart_data(current_user, db: Session):
    histories = (
        db.query(TestHistory)
        .filter(TestHistory.user_id == current_user.id)
        .order_by(TestHistory.taken_at)
        .all()
    )
    return [
        {
            "lesson_id": h.lesson_id,
            "score": h.score,
            "date": h.taken_at.strftime("%Y-%m-%d %H:%M")
        }
        for h in histories
    ]


def evaluate_quiz(lesson_id: int, answers: dict, user_id: int, db: Session):
    # Savollarni olish
    questions = db.query(Quiz).filter(Quiz.lesson_id == lesson_id).all()

    if not questions:
        raise HTTPException(404, detail="Bu dars uchun testlar topilmadi.")

    total = len(questions)
    correct = 0

    for question in questions:
        user_answer = answers.get(str(question.id))
        if user_answer and user_answer == question.correct_answer:
            correct += 1

    score = round((correct / total) * 100, 2)

    # Saqlash
    history = TestHistory(
        user_id=user_id,
        lesson_id=lesson_id,
        score=score,
        taken_at=datetime.now(pytz.timezone("Asia/Tashkent"))
    )

    db.add(history)
    db.commit()
    db.refresh(history)

    return {
        "score": score,
        "correct_answers": correct,
        "total_questions": total
    }
