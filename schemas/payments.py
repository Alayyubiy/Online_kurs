from pydantic import BaseModel

class CreatePayment(BaseModel):
    user_id: int
    course_id: int
    amount: float
