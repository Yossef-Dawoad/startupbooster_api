from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = ""
    disabled: Optional[bool] = False


class UserCreateSchema(UserBase):
    password: str


class UserSchema(UserBase):
    id: int
    createdAt: datetime

    class Config:
        orm_mode = True


class AuthenticatedUserSchema(UserSchema):
    hashed_password: str
