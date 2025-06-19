from pydantic import BaseModel, Field

class CreateUser(BaseModel):
    name: str
    username: str
    password: str = Field(min_length=4, max_length=8)
    phone: str

class UpdateUser(BaseModel):
    name: str
    username: str
    password: str = Field(min_length=4, max_length=8)
    phone: str