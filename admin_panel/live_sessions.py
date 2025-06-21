from sqladmin import ModelView
from starlette.requests import Request

from models.live_sessions import LiveSession

class LiveSessionAdmin(ModelView, model=LiveSession):
    name = "Live Session"
    name_plural = "Live Sessions"
    icon = "fa-solid fa-video"
    page_size = 10

    column_list = ["title", "host", "course", "start_time", "room_link"]
    form_columns = ["title", "host", "course", "start_time", "room_link"]

    column_labels = {
        "title": "Sarlavha",
        "host": "Ustoz",
        "course": "Kurs",
        "start_time": "Boshlanish vaqti",
        "room_link": "Vidiochat linki"
    }

    column_searchable_list = ["title", "room_link"]
    column_sortable_list = ["start_time"]


    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True