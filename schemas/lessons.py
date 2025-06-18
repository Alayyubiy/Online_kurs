from pydantic import BaseModel

class CreateLessons(BaseModel):
    title:str
    video_url:str
    sections_id:int
    order:int
    homework_file_url:str



class UpdateLessons(BaseModel):
    title:str
    video_url:str
    sections_id:int
    order:int
    homework_file_url:str