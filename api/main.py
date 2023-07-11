from collections.abc import Generator
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine, sessionLocal
from .utils import generate_business_snippet, generate_keywords

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Brand Booster API",
    description="""
    Brand Booster generate catchy tagline
    with SEO optimized keywords for your business.""",
    version="0.1.3", #[TODO] 0.2.0 authentications
    contact={
        "name": "Yousef Dawoud",
        "email": "yousefdawoud.dev@outlook.com",
    },
)


# Dependency
def get_db() -> Generator:
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World!"}


@app.post(
    "/api/v2/businesses/",
    response_model=schemas.BusinessModel,
    status_code=201,
)
def create_business(
    business: schemas.BusinessModelCreate,
    db: Annotated[Session, Depends(get_db)],
) -> models.Bussiness:
    db_business = crud.get_businessModel(db, business_name=business.name)
    if db_business:
        #[TODO] return the element in the database if not auth
        raise HTTPException(
            status_code=400, detail="Business Name already registered",
        )

    business_snippet = generate_business_snippet(business.name)
    business_keywords = generate_keywords(business.name)
    return crud.create_business(
        db=db,
        business=business,
        snippet=business_snippet,
        keywords=business_keywords["kw"],
    )


@app.get("/api/v2/businesses/", response_model=list[schemas.BusinessModel])
def read_business(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
) -> list[models.Bussiness]:
    businesses = crud.get_business(db, skip=skip, limit=limit)
    return businesses


################################ api/ver 1 - no database ######################
StringArray = list[str]


@app.get("/api/v1/keywords")
def api_generate_keywords(prompt: str) -> dict[str, StringArray]:
    llm_result = generate_keywords(prompt)
    return llm_result


@app.get("/api/v1/snippets")
def api_generate_snippets(prompt: str) -> str:
    llm_result = generate_business_snippet(prompt)
    return llm_result


@app.get("/api/v1/business/")
def api_generate_business_seo(prompt: str) -> dict[str, Any]:
    business_keywords = generate_keywords(prompt)
    business_snippet = generate_business_snippet(prompt)
    return {
        "snippets": business_snippet,
        "keywords": business_keywords["Keywords"],
    }
