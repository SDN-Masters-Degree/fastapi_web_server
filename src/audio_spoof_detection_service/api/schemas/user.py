from datetime import datetime

from pydantic import BaseModel, EmailStr


class RegisterUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class RegisterUserResponse(BaseModel):
    username: str
    email: str
    registered_at: datetime


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str


class LoginUserResponse(BaseModel):
    access_token: str
    refresh_token: str


class LogoutUserRequest(BaseModel):
    refresh_token: str


class LogoutUserResponse(BaseModel):
    message: str


class GetUserInfoResponse(BaseModel):
    user_id: int
    username: str
    email: str
    registered_at: datetime


class RefreshTokensRequest(BaseModel):
    refresh_token: str


class RefreshTokensResponse(BaseModel):
    access_token: str
    refresh_token: str
