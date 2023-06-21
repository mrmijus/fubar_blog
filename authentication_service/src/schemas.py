from datetime import datetime
from pydantic import BaseModel


class Message(BaseModel):
    message: str


class LoginRequest(BaseModel):
    email: str
    password: str


class User(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True