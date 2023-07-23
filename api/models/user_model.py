from datetime import datetime
from typing import Annotated

import sqlalchemy as sa
from passlib.hash import bcrypt
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry
from sqlalchemy.sql import func

str30 = Annotated[str, 30]
str50 = Annotated[str, 50]


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            str30: sa.String(30),
            str50: sa.String(50),
        },
    )


intpk = Annotated[int, mapped_column(primary_key=True)]
text = Annotated[str, mapped_column(sa.String, nullable=False)]
boolType = Annotated[bool, mapped_column(sa.Boolean, default=False)]
timeNow = Annotated[
    datetime,
    mapped_column(sa.DateTime(timezone=True), default=func.now()),
]


class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk]  # ✨
    username: Mapped[str30]  # ✨✨
    full_name: Mapped[str50]  # ✨✨
    email: Mapped[text]  # ✨✨✨
    hashed_password: Mapped[text]  # ✨✨✨
    createdAt: Mapped[timeNow]  # ✨✨✨✨
    disabled: Mapped[boolType]  # ✨✨✨

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def verify_passcode(self, password: str) -> bool:
        return bcrypt.verify(password, self.hashed_password)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email
        return False
