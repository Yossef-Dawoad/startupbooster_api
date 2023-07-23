from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = ""
    disabled: bool | None = False


class UserCreateSchema(UserBase):
    password: str


class UserSchema(UserBase):
    id: int

    class Config:
        orm_mode = True


class AuthenticatedUserSchema(UserSchema):
    hashed_password: str
