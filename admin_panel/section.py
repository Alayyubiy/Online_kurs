from sqladmin import ModelView
from models.section import Section
from starlette.requests import Request

class SectionAdmin(ModelView, model=Section):
    column_list = [
        "title", "order", "course"
    ]
    form_columns = [
        "title", "order", "course"
    ]
    name = "Section"
    name_plural = "Section"
    icon = "fa-solid fa-clock-rotate-left"

    column_sortable_list = [
        "section.id"

    ]

    column_labels = {
        "title": "Title",
        "order": "Order",
        "course": "Course",


    }

    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True