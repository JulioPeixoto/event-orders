from typing import Optional
from sqlmodel import SQLModel
from pydantic import EmailStr


class UserBase(SQLModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None


class UserPublic(UserBase):
    id: int
    is_active: bool


class UserLogin(SQLModel):
    username: str
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(SQLModel):
    user_id: Optional[int] = None
