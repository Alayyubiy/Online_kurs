from pydantic import BaseModel

class CourseImageBase(BaseModel):
    image: str

class CourseImageCreate(CourseImageBase):
    course_id: int

class CourseImageOut(CourseImageBase):
    id: int
    course_id: int

    class Config:
        orm_mode = True