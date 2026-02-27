from models.course import Course
from admin_panel._secure_base import SecureAdminView


class CourseAdmin(SecureAdminView, model=Course):
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