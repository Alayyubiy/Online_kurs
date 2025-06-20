from sqladmin import ModelView
from models.enrollment import Enrollment
from starlette.requests import Request

class EnrollmentAdmin(ModelView, model=Enrollment):
    column_list = [
        "user", "course","enrolled_at"
    ]
    form_columns = [
         "user", "course"
    ]


    name = "Enrollment"
    name_plural = "Enrollment"
    page_size = 10
    icon = "fa-regular fa-file"

    column_sortable_list = [
        "enrollments.id"

    ]

    column_labels = {
        "user": "User",
        "course": "Course"

    }

    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True
