import asyncio
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, models, schemas
from .database import async_get_db
from .utils import generate_business_snippet, generate_keywords

app = FastAPI(
    title="Brand Booster API",
    description="""
    Brand Booster generate catchy tagline
    with SEO optimized keywords for your business.""",
    version="0.2.1",  # [TODO] 0.3.0 authentications
    contact={
        "name": "Yousef Dawoud",
        "email": "yousefdawoud.dev@outlook.com",
    },
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World!"}


@app.post(
    "/api/v2/businesses",
    response_model=schemas.BusinessModel,
    status_code=201,
)
async def create_business(
    business: schemas.BusinessModelCreate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> models.Bussiness:
    db_business = await crud.get_businessModel(db, business_name=business.name)
    if db_business:
        # [TODO] return the element in the database if not auth
        raise HTTPException(
            status_code=400,
            detail="Business Name already registered",
        )

    brandMaker_funcs = [generate_business_snippet, generate_keywords]
    tasks = [  # Wait for the tasks to finish using asyncio.gather()
        asyncio.create_task(func(business.name)) for func in brandMaker_funcs
    ]
    # Wait for the tasks to finish using asyncio.gather()
    results = await asyncio.gather(*tasks)
    results_dict = {
        func.__name__: result for func, result in zip(brandMaker_funcs, results)
    }
    return await crud.create_business(
        db=db,
        business=business,
        snippet=results_dict["generate_business_snippet"],
        keywords=results_dict["generate_keywords"]["kw"],
    )


@app.get("/api/v2/businesses", response_model=list[schemas.BusinessModel])
async def read_businesses(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(async_get_db),
) -> list[models.Bussiness]:
    businesses = await crud.get_business(db, skip=skip, limit=limit)
    return businesses


@app.get("/api/v2/businesses/{id}", response_model=schemas.BusinessModel)
async def read_business(
    id: int,
    db: AsyncSession = Depends(async_get_db),
) -> list[models.Bussiness]:
    businessdb = await crud.get_businessModelbyId(db, id)
    if not businessdb:
        raise HTTPException(
            status_code=404,
            detail=f"Business with this Id of {id} not exist",
        )
    return businessdb


################################ api/ver 1 - no database ######################
StringArray = list[str]


@app.get("/api/v1/keywords")
async def api_generate_keywords(prompt: str) -> dict[str, StringArray]:
    llm_result = await generate_keywords(prompt)
    return llm_result


@app.get("/api/v1/snippets")
async def api_generate_snippets(prompt: str) -> str:
    llm_result = await generate_business_snippet(prompt)
    return llm_result


@app.get("/api/v1/business")
async def api_generate_business_seo(prompt: str) -> dict[str, Any]:
    brandMaker_funcs = [generate_business_snippet, generate_keywords]
    tasks = [  # Wait for the tasks to finish using asyncio.gather()
        asyncio.create_task(func(prompt)) for func in brandMaker_funcs
    ]
    results = await asyncio.gather(*tasks)
    results_dict = {
        func.__name__: result for func, result in zip(brandMaker_funcs, results)
    }
    return {
        "snippets": results_dict["generate_business_snippet"],
        "keywords": results_dict["generate_keywords"]["kw"],
    }
