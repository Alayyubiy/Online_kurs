import datetime
from pydantic import BaseModel

class CreateProgress(BaseModel):
    user_id:int
    lessons_id:int
    completed:bool
    completed_at:datetime


class UpdateProgress(BaseModel):
    user_id:int
    lessons_id:int
    completed:bool
    completed_at:datetime