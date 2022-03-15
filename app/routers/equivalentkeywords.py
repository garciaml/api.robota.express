from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, engine
from typing import List, Optional
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
@router.get(
    "/{label}",
    response_model=schemas.EquivalentKeyword,
    summary="get equivalent keyword by label",
)
def read_equikeyword_label(label: str, db: Session = Depends(get_db)):
    db_equikeyword = crud.get_equikeywords_by_label(db, label=label)
    if db_equikeyword is None:
        raise HTTPException(status_code=404, detail="Equivalent Keyword not found")
    return db_equikeyword

@router.get(
    "/",
    response_model=List[schemas.EquivalentKeyword],
    summary="get equivalent keyword by attributes",
)
def read_equikeyword_keyword(keyword: Optional[str] = None, refugee_id: Optional[int] = None, db: Session = Depends(get_db)):
    db_equikeyword = crud.get_equikeywords_by_attributes(db, {"keyword": keyword})
    if db_equikeyword is None:
        raise HTTPException(status_code=404, detail="Equivalent Keyword not found")
    # The dictionary "attributes" must not contain None values 
    attributes = {}
    if keyword:
        attributes["keyword"] = keyword
    if refugee_id:
        attributes["refugee_id"] = refugee_id
    db_equikeyword = crud.get_equikeywords_by_attributes(db, attributes=attributes)
    return db_equikeyword
