# SQLAlchemy
# https://devblog.dunsap.com/2022/11-11---using-alembic-with-with-sqlalchemy-2/

from datetime import datetime
from typing import Annotated

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry
from sqlalchemy.sql import func

str30 = Annotated[str, 30]


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            str30: sa.String(30),
        },
    )


# set up mapped_column() overrides, using whole column styles that are
# expected to be used in multiple places
intpk = Annotated[int, mapped_column(primary_key=True)]
text = Annotated[str, mapped_column(sa.String, nullable=False)]
pklStringList = Annotated[
    list[str],
    mapped_column(sa.PickleType, nullable=False),
]
business_fk = Annotated[int, mapped_column(sa.ForeignKey("business.id"))]
timeNow = Annotated[
    datetime,
    mapped_column(sa.DateTime(timezone=True), default=func.now()),
]


class Bussiness(Base):
    __tablename__ = "business"

    id: Mapped[intpk]  # ✨
    name: Mapped[str30]  # ✨✨
    snippet: Mapped[text]  # ✨✨✨
    keywords: Mapped[pklStringList]  # ✨✨✨
    createdAt: Mapped[timeNow]  # ✨✨✨✨

    def __repr__(self) -> str:  # noqa: ANN101
        str_obj = f"""
Business {self.name}
-----
the tagline:
{self.snippet[:100]}....
-----
keywords
-----
{self.keywords[:4]}....
"""
        return str_obj


# class Keyword(Base):
#  __tablename__ = "keywords"

#     id: Mapped[intpk]
#     name: Mapped[str30]
#     business_id: Mapped[business_fk]
#     business: Mapped["Bussiness"] = relationship(back_populates="keywords")
