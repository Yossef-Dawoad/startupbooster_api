# # valided our data to make sure it valid to be added to the database tables
from datetime import datetime

from pydantic import BaseModel

############################## businesses schema Model ########################


class BusinessModelBase(BaseModel):
    name: str


class BusinessModelCreate(BusinessModelBase):
    pass


class BusinessModel(BusinessModelBase):
    id: int
    snippet: str
    keywords: list[str]
    createdAt: datetime | None = None

    class Config:
        orm_mode = True
