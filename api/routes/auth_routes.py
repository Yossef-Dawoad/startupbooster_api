from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import async_get_db
from ..models.user_model import User
from ..schemas.token_schema import TokenSchema
from ..schemas.user_schema import AuthenticatedUserSchema, UserCreateSchema, UserSchema
from ..utils.authentication import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_hashed_passcode,
    get_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/token", response_model=TokenSchema)
async def generate_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
        "token_type": "bearer",
    }


@router.post("/register", response_model=UserSchema)
async def create_user(
    user_inp: UserCreateSchema,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> User:
    user = await get_user(db, user_name=user_inp.username)
    if user:
        raise HTTPException(status_code=400, detail="username already registered")
    hashed_password = get_hashed_passcode(user_inp.password)
    db_user = User(
        **user_inp.dict(exclude={"password"}),
        hashed_password=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.get("/users/me")
async def get_user_signed(
    user: Annotated[AuthenticatedUserSchema, Depends(get_current_user)],
) -> dict[str, str]:
    return {
        "conversation": "This is a secure conversation!",
        "current_user": user.username,
    }
