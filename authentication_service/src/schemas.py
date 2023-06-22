from typing import Any
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


class UserRegistration(BaseModel):
    username: str
    password: str
    email: str

    class Config:
        orm_mode = True


class VerifyToken(BaseModel):
    token: str


class FullUser(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    user_role: str
    status: str
