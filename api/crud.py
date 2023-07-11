# ruff: enable=type_checking,type_annotations
from sqlalchemy.orm import Session

from . import models, schemas


def get_businessModel(
    db: Session, business_name: str,
) -> models.Bussiness | None:
    return (
        db.query(models.Bussiness)
        .filter(models.Bussiness.name == business_name)
        .first()
    )


################################# Business Model ##############################
def get_business(
    db: Session, skip: int = 0, limit: int = 10,
) -> list[models.Bussiness]:
    return db.query(models.Bussiness).offset(skip).limit(limit).all()


def create_business(
    db: Session,
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
    db.commit()
    db.refresh(db_business)
    return db_business
