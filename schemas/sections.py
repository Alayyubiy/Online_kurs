from pydantic import BaseModel


class CreateSections(BaseModel):
    title:str
    course_id:int
    order:int



class UpdateSections(BaseModel):
    title: str
    course_id: int
    order: int


