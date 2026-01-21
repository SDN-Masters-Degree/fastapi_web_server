from datetime import datetime

from pydantic import BaseModel, EmailStr


class RegisterUserRequest(BaseModel):
    username: str
    email: EmailStr


class RegisterUserResponse(BaseModel):
    username: str
    email: EmailStr
    registered_at: datetime


class LoginUserRequest(BaseModel):
    email: EmailStr
    one_time_password: str


class LoginUserResponse(BaseModel):
    access_token: str
    refresh_token: str
