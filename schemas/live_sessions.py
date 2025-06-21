from pydantic import BaseModel
from datetime import datetime

class CreateLiveSession(BaseModel):
    title: str
    course_id: int
    start_time: datetime
    room_link: str
