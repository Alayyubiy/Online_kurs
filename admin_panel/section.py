from models.section import Section
from admin_panel._secure_base import SecureAdminView


class SectionAdmin(SecureAdminView, model=Section):
    column_list = [
        "title", "order", "course"
    ]
    form_columns = [
        "title", "order", "course"
    ]
    name = "Section"
    name_plural = "Section"
    column_searchable_list = [Section.title]
    page_size = 10
    icon = "fa-solid fa-clock-rotate-left"

    column_sortable_list = [
        "section.id"
    ]

    column_labels = {
        "title": "Title",
        "order": "Order",
        "course": "Course",
    }