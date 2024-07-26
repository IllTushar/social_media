from pydantic import BaseModel, EmailStr
from datetime import date


class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str
    DOB: date


class ResponseUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str
    DOB: date

    class Config:
        orm_mode = True
