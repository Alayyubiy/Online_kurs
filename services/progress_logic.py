from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.test_history import TestHistory
from models.lesson import Lesson


def check_section_completion(user_id: int, section_id: int, db: Session):
    # Shu sectionga tegishli barcha lessonlarni olish
    lesson_ids = db.query(Lesson.id).filter(Lesson.section_id == section_id).all()
    lesson_ids = [lid[0] for lid in lesson_ids]

    if not lesson_ids:
        raise HTTPException(404, detail="Ushbu sectionda darslar mavjud emas.")

    # Shu foydalanuvchining o‘sha darslardagi test natijalarini olish
    scores = (
        db.query(func.avg(TestHistory.score))
        .filter(
            TestHistory.user_id == user_id,
            TestHistory.lesson_id.in_(lesson_ids)
        )
        .scalar()
    )

    if scores is None:
        raise HTTPException(400, detail="Foydalanuvchi hali bu sectiondagi testlarni ishlamagan.")

    if scores >= 60:
        return {"status": "pass", "average_score": round(scores, 2), "message": "Tabriklaymiz! Siz keyingi bo‘limga o‘ta olasiz."}
    else:
        return {"status": "fail", "average_score": round(scores, 2), "message": "Iltimos, bu bo‘limni qayta o‘qing va testlarni takrorlang."}
