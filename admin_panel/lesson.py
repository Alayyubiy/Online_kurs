from models.lesson import Lesson
from admin_panel._secure_base import SecureAdminView


class LessonAdmin(SecureAdminView, model=Lesson):
    column_list = [
        "section", "title", "video_url", "homework_file_url", "order"
    ]
    form_columns = [
        "section", "title", "video_url", "homework_file_url", "order"
    ]
    form_widget_args = {
        "homework_file_url": {
            "type": "file"
        },
        "video_url": {
            "type": "file"
        }
    }

    name = "Lesson"
    name_plural = "Lesson"
    column_searchable_list = [Lesson.title]
    page_size = 10
    icon = "fa-solid fa-person-chalkboard"

    column_sortable_list = [
        "lesson.id"
    ]

    column_labels = {
        "section": "Section",
        "title": "Title",
        "video_url": "Video_url",
        "homework_file_url": "Homework_file_url",
        "order": "Order",
    }