from sqladmin import ModelView
from models.test_history import TestHistory
from starlette.requests import Request

class HistoryAdmin(ModelView, model=TestHistory):
    column_list = [
        "user", "lesson", "score", "total_questions", "correct_answers", "taken_at"
    ]
    form_columns = [
        "user", "lesson", "score", "total_questions", "correct_answers", "taken_at"
    ]
    name = "TestHistory"
    name_plural = "TestHistory"
    icon = "fa-solid fa-clock-rotate-left"

    column_sortable_list = [
        "test_history.id"

    ]

    column_labels = {
        "user": "User",
        "lesson": "Lesson",
        "score": "Score",
        "total_questions": "Total_questions",
        "correct_answers": "Correct_answers",
        "taken_at": "Taken_at",

    }

    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True
