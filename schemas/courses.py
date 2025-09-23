from pydantic import BaseModel


class CreateCourses(BaseModel):
    name:str
    description:str
    category:str
    duration:str
    level:str
    price:int
    teacher:str


class UpdateCourses(BaseModel):
    name:str
    description:str
    category:str
    duration:str
    level:str
    price:int
    teacher:str



