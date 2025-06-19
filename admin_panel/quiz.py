from sqladmin import ModelView
from models.quiz import Quiz
from starlette.requests import Request

class QuizAdmin(ModelView, model=Quiz):
    column_list = [
        "lesson", "question", "correct_answer"
    ]
    form_columns = [
         "lesson", "question", "correct_answer"
    ]
    name = "Quiz"
    name_plural = "Quiz"
    icon = "fa-solid fa-circle-question"

    column_sortable_list = [
        "quiz.id"

    ]

    column_labels = {
        "lesson": "Lesson",
        "question": "Question",
        "correct_answer": "Correct_answer",


    }

    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True