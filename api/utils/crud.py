# ruff: enable=type_checking,type_annotations
from typing import Union  # for py39

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import business_model
from ..schemas.business_schema import BusinessModelCreate


async def get_businessModel(
    db: AsyncSession,
    business_name: str,
) -> Union[business_model.Bussiness, None]:  # noqa: UP007
    business = await db.execute(
        sa.select(business_model.Bussiness).filter(
            business_model.Bussiness.name == business_name,
        ),
    )
    return business.scalar_one_or_none()


async def get_businessModelbyId(
    db: AsyncSession,
    business_id: int,
) -> Union[business_model.Bussiness, None]:  # noqa: UP007
    business = await db.execute(
        sa.select(business_model.Bussiness).filter(
            business_model.Bussiness.id == business_id,
        ),
    )
    return business.scalar_one_or_none()


################################# Business Model ##############################
async def get_business(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
) -> list[business_model.Bussiness]:
    # businesses =  db.query(models.Bussiness).offset(skip).limit(limit).all()
    businesses = await db.execute(
        sa.select(business_model.Bussiness).offset(skip).limit(limit),
    )
    return businesses.scalars().all()


async def create_business(
    db: AsyncSession,
    business: BusinessModelCreate,
    snippet: str,
    keywords: list[str],
) -> business_model.Bussiness:
    db_business = business_model.Bussiness(
        name=business.name,
        snippet=snippet,
        keywords=keywords,
    )
    db.add(db_business)
    await db.commit()
    await db.refresh(db_business)
    return db_business
