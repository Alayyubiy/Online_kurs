from models.user import User
from admin_panel._secure_base import SecureAdminView


class UserAdmin(SecureAdminView, model=User):
    column_list = [User.id, User.name, User.username, User.phone, User.role]
    # ✅ User.password olib tashlandi - admin panelda parol ko'rinmasin!
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    column_searchable_list = [User.name]
    page_size = 10
    page_size_options = [10, 20, 50]