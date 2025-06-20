from sqladmin import ModelView
from models.course import Course
from starlette.requests import Request

class CourseAdmin(ModelView, model=Course):
    column_list = [
        "name", "description", "data_time"
    ]
    form_columns = [
        "name", "description"
    ]
    name = "Course"
    name_plural = "Course"
    column_searchable_list = [Course.name]
    page_size = 10
    icon = "fa-regular fa-bell"

    column_sortable_list = [
        "Course.id"

    ]

    column_labels = {
        "name": "Name",
        "description": "Description",
        "data_time": "Data_time",

    }

    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True
