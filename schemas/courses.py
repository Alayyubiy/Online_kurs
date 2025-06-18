from datetime import datetime
from pydantic import BaseModel


class CreateCourses(BaseModel):
    name:str
    description:str



class UpdateCourses(BaseModel):
    name:str
    description:str


class CourseOut(BaseModel):
    id: int
    data_time: datetime
