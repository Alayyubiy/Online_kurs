from sqladmin import ModelView
from models.progress import Progress
from starlette.requests import Request

class ProgressAdmin(ModelView, model=Progress):
    column_list = [
        "lesson", "question", "correct_answer"
    ]
    form_columns = [
         "lesson", "question", "correct_answer"
    ]
    name = "Progress"
    name_plural = "Progress"
    icon = "fa-solid fa-bars-progress"

    column_sortable_list = [
        "progress.id"

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