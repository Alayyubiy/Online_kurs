from typing import Optional

from pydantic import BaseModel, Field


class CreatePayment(BaseModel):
    user_id: int
    course_id: int
    amount: float

class UpdatePaymentStatus(BaseModel):
    payment_id: int
    new_status: Optional[str] = Field(None, description="Yangi holat: 'paid', 'pending', 'failed'")
    new_amount: Optional[float] = Field(None, description="Yangi to'lov miqdori (ixtiyoriy)")