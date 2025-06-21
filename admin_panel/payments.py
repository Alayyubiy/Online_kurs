from datetime import datetime

import pytz
from sqladmin import ModelView
from models.payments import Payment
from starlette.requests import Request

class PaymentAdmin(ModelView, model=Payment):



    column_list = [
        "user", "course","amount","status","paid_at"
    ]


    form_columns = [
        "user", "course", "amount", "status"
    ]



    name = "Payment"
    column_searchable_list = ["user.name", "course.name"]
    column_filters = ["status", "course_id", "user_id"]

    name_plural = "Payment"
    page_size = 10
    icon = "fa-solid fa-money-check-dollar"

    column_sortable_list = [
        "payment.id"

    ]

    column_labels = {
        "user": "User",
        "course": "Course",
        "amount":"Amount",
        "status":"Status",
        "pait_at":"Pait_at"


    }

    async def on_model_change(self, request, model, form, is_created):
        if model.status == "paid":
            model.paid_at = datetime.now(pytz.timezone("Asia/Tashkent"))
        else:
            model.paid_at = None


    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True
