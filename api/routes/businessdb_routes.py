import asyncio
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

# from ...database import async_get_db
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, models, schemas
from ..database import async_get_db
from ..utils import generate_business_snippet, generate_keywords

router = APIRouter(
    prefix="/api/v2",
    tags=["Businesses /w DataBase"],
)

log = logging.getLogger("api-routes-logs")


@router.post(
    "/businesses",
    response_model=schemas.BusinessModel,
)
async def create_business(
    business: schemas.BusinessModelCreate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> models.Bussiness:
    db_business = await crud.get_businessModel(db, business_name=business.name)
    # [TODO] This just testing should be removed [Sensetive]
    log.debug(db_business)
    # [TODO] we need a way to tell if it's created or fetched from the db
    if db_business:
        log.warning("fetch-ing from the database")
        return db_business

    brandMaker_funcs = [generate_business_snippet, generate_keywords]
    tasks = [  # Wait for the tasks to finish using asyncio.gather()
        asyncio.create_task(func(business.name)) for func in brandMaker_funcs
    ]
    # Wait for the tasks to finish using asyncio.gather()
    results = await asyncio.gather(*tasks)
    results_dict = {
        func.__name__: result for func, result in zip(brandMaker_funcs, results)
    }

    db_business = await crud.create_business(
        db=db,
        business=business,
        snippet=results_dict["generate_business_snippet"],
        keywords=results_dict["generate_keywords"]["kw"],
    )
    log.debug(db_business)
    return db_business


@router.get("/businesses", response_model=list[schemas.BusinessModel])
async def read_businesses(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(async_get_db),
) -> list[models.Bussiness]:
    businesses = await crud.get_business(db, skip=skip, limit=limit)
    return businesses


@router.get("/businesses/{id}", response_model=schemas.BusinessModel)
async def read_business(
    id: int,
    db: AsyncSession = Depends(async_get_db),
) -> list[models.Bussiness]:
    db_business = await crud.get_businessModelbyId(db, id)
    log.debug(db_business)
    if not db_business:
        raise HTTPException(
            status_code=404,
            detail=f"Business with this Id of {id} not exist",
        )
    return db_business
