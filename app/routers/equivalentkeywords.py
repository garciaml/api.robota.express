from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, engine
from typing import List
from datetime import date

# router = APIRouter()
router = APIRouter(
    prefix="/equikeywords",
    tags=["Equivalent Keywords"],
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


### Create a new equivalent keyword

@router.post(
    "/", 
    response_model=schemas.EquivalentKeyword,
)
def create_equikeyword(equikeyword: schemas.EquivalentKeyword, db: Session = Depends(get_db)):
    db_equikeyword = crud.get_equikeywords_by_label(db, label=equikeyword.label)
    if db_equikeyword:
        raise HTTPException(status_code=400, detail="Equivalent Keyword already existing")
    db_equikeyword_keyword = crud.get_keywords_by_label(db, label=equikeyword.keyword)
    if db_equikeyword_keyword:
        return crud.create_equikeyword(db=db, equikeyword=equikeyword)
    else:
        raise HTTPException(status_code=404, detail="Keyword does not exist. Please create keyword before")


### Find a Keyword by label
path = "/"
@router.get(
    path + "{label}",
    response_model=schemas.EquivalentKeyword,
    summary="get equivalent keyword by label",
)
def read_equikeyword_label(label: str, db: Session = Depends(get_db)):
    db_equikeyword = crud.get_equikeywords_by_label(db, label=label)
    if db_equikeyword is None:
        raise HTTPException(status_code=404, detail="Equivalent Keyword not found")
    return db_equikeyword
path += "label/"

@router.get(
    path + "{keyword}",
    response_model=List[schemas.EquivalentKeyword],
    summary="get equivalent keyword by keyword",
)
def read_equikeyword_keyword(keyword: str, db: Session = Depends(get_db)):
    db_equikeyword = crud.get_equikeywords_by_keyword(db, keyword=keyword)
    if db_equikeyword is None:
        raise HTTPException(status_code=404, detail="Equivalent Keyword not found")
    return db_equikeyword
path += "keyword/"
