from pydantic import BaseModel
from datetime import datetime


class TestHistoryOut(BaseModel):
    id: int
    user_id: int
    lesson_id: int
    score: float
    total_questions: int
    correct_answers: int
    taken_at: datetime

    class Config:
        orm_mode = True


class TopStudentOut(BaseModel):
    user_id: int
    name: str
    avg_score: float
