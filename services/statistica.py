# services/statistics.py
from sqlalchemy.orm import Session
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
