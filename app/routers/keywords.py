from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, engine
from typing import List
from datetime import date

# router = APIRouter()
router = APIRouter(
    prefix="/keywords",
    tags=["Keywords"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# TODO:
# - update category
# - delete a keyword

### Create a new keyword

@router.post(
    "/", 
    response_model=schemas.Keyword,
)
def create_keyword(keyword: schemas.Keyword, db: Session = Depends(get_db)):
    db_keyword = crud.get_keywords_by_label(db, label=keyword.label)
    if db_keyword:
        raise HTTPException(status_code=400, detail="Keyword already existing")
    return crud.create_keyword(db=db, keyword=keyword)

### Find a Keyword by label
path = "/"
@router.get(
    path + "{label}",
    response_model=schemas.Keyword,
    summary="get keyword by label",
)
def read_keyword_label(label: str, db: Session = Depends(get_db)):
    db_keyword = crud.get_keywords_by_label(db, label=label)
    if db_keyword is None:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return db_keyword

