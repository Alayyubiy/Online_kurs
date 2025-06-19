from sqladmin import ModelView
from models.user import User
from starlette.requests import Request

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name, User.username, User.password]
    name = "User"
    name_plural = "User"
    icon = "fa-solid fa-user"
    column_searchable_list = [User.name]
    page_size = 10
    page_size_options = [10, 20, 50]

    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True