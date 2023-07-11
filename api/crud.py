# ruff: enable=type_checking,type_annotations
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_businessModel(
    db: AsyncSession,
    business_name: str,
) -> (models.Bussiness | None):
    business = await db.execute(
        sa.select(models.Bussiness).filter(models.Bussiness.name == business_name),
    )
    return business.scalar_one_or_none()


async def get_businessModelbyId(
    db: AsyncSession,
    business_id: int,
) -> (models.Bussiness | None):
    business = await db.execute(
        sa.select(models.Bussiness).filter(models.Bussiness.id == business_id),
    )
    return business.scalar_one_or_none()


################################# Business Model ##############################
async def get_business(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
) -> list[models.Bussiness]:
    # businesses =  db.query(models.Bussiness).offset(skip).limit(limit).all()
    businesses = await db.execute(
        sa.select(models.Bussiness).offset(skip).limit(limit),
    )
    return businesses.scalars().all()


async def create_business(
    db: AsyncSession,
    business: schemas.BusinessModelCreate,
    snippet: str,
    keywords: list[str],
) -> models.Bussiness:
    db_business = models.Bussiness(
        name=business.name,
        snippet=snippet,
        keywords=keywords,
    )
    db.add(db_business)
    await db.commit()
    await db.refresh(db_business)
    return db_business
