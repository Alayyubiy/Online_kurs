from datetime import datetime
from pydantic import BaseModel


class  CreateEnrollments(BaseModel):
    user_id:int
    course_id:int
    enrolled_at:datetime


class  UpdateEnrollments(BaseModel):
    user_id:int
    course_id:int
    enrolled_at:datetime