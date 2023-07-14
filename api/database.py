# the backbone of how to connect and use the database


import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from api.models import Base

load_dotenv()


Async_DATABASE_URL = os.environ["ASYNC_DB_URL"]
Async_Engine = create_async_engine(
    Async_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
Async_sessionLocal = async_sessionmaker(
    bind=Async_Engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# Dependency
async def async_get_db() -> Generator:
    async with Async_Engine.begin() as aconn:
        await aconn.run_sync(Base.metadata.create_all)
    # [TODO] check for this sentax
    # async with Async_sessionLocal() as adb:
    #     yield adb
    #     await adb.commit()
    db = Async_sessionLocal()
    try:
        yield db
    finally:
        await db.close()
