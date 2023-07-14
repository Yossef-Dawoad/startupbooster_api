import asyncio
import logging
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from api.logs.apilogconfig import init_loggers

from . import crud, models, schemas
from .database import async_get_db
from .utils import generate_business_snippet, generate_keywords

# TODO REMOVE any senetive logging
# LOGs - This should run as soon as possible to catch all logs
# Run only one of these
init_loggers(logger_name="api-routes-logs")
app = FastAPI(
    title="Brand Booster API",
    description="""
    Brand Booster generate catchy tagline
    with SEO optimized keywords for your business.""",
    version="0.2.3",  # [TODO] 0.3.0 authentications
    contact={
        "name": "Yousef Dawoud",
        "email": "yousefdawoud.dev@outlook.com",
    },
)

# init our logger
log = logging.getLogger("api-routes-logs")

# [UPDATE] CORS Setup
origins = [
    # "http://localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World!"}


@app.get("/logs")
def log_now() -> dict[str, str]:
    log.debug("Successfully hit the /log endpoint.")
    return {"result": "OK"}


@app.post(
    "/api/v2/businesses",
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
