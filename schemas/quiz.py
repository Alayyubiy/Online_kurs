from pydantic import BaseModel
from typing import Dict

class CreateQuiz(BaseModel):
    lesson_id: int
    question: str
    correct_answer: str

class QuizAnswer(BaseModel):
    answers: Dict[int, str]  # {quiz_id: "user_answer"}
