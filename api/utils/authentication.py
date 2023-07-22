import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

import sqlalchemy as sa
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import async_get_db
from ..models.user_model import User

SECRET_KEY = os.getenv("SECRET_KEY")
JWT_REFRESH_SECRET_KEY = os.environ["JWT_REFRESH_SECRET_KEY"]
HASH_ALGORITHEM = os.getenv("HASH_ALGORITHEM")
ACCESS_TOKEN_EXPIRE_MIN = 30
REFRESH_TOKEN_EXPIRE_TIME = 60 * 24 * 7  # 7 days


pass_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def verify_passcode(plain: str, hashed: str) -> bool:
    return pass_ctx.verify(plain, hashed)


def get_hashed_passcode(plain: str) -> str:
    return pass_ctx.hash(plain)


def create_access_token(
    subject: str | Any,
    expires_delta: timedelta | None = None,
) -> str:
    if not expires_delta:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    expire_time = datetime.now(tz=timezone.utc) + expires_delta
    to_encode = {"exp": expire_time, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, HASH_ALGORITHEM)
    return encoded_jwt


def create_refresh_token(
    subject: str | Any,
    expires_delta: timedelta | None = None,
) -> str:
    if not expires_delta:
        expires_delta = timedelta(minutes=REFRESH_TOKEN_EXPIRE_TIME)
    expire_time = datetime.now(tz=timezone.utc) + expires_delta
    to_encode = {"exp": expire_time, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, HASH_ALGORITHEM)
    return encoded_jwt


def unauth_exception_error(
    detail: str = "Invalid authentication credentials",
    headers: dict = {"WWW-Authenticate": "Bearer"},
) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers=headers,
    )


async def get_user(db: AsyncSession, user_name: str) -> User | None:
    user = await db.execute(
        sa.select(User).filter(User.username == user_name),
    )
    return user.scalars().one_or_none()


async def authenticate_user(
    db: AsyncSession,
    user_name: str,
    password: str,
) -> User | None:
    user = await get_user(db, user_name)
    if not user or not user.verify_passcode(password):
        return None
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH_ALGORITHEM])
        user = await get_user(db, user_name=payload.get("sub"))

        if user is None:
            raise unauth_exception_error()
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentecation error: Invalid username or password",
        )

    return user
