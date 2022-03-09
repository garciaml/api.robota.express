from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, engine
from typing import List
from datetime import date

# router = APIRouter()
router = APIRouter(
    prefix="/refugees",
    tags=["Refugees"],
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


### Create a new refugee

@router.post(
    "/", 
    response_model=schemas.Refugee,
)
def create_refugee(refugee: schemas.Refugee, db: Session = Depends(get_db)):
    db_user = crud.get_refugees_by_email(db, email=refugee.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_refugee(db=db, refugee=refugee)


### Find refugee
path = "/"
# By identifier
@router.get(
    path + "{id}",
    response_model=schemas.Refugee,
    summary="get refugee by identifier",
)
def read_refugee_id(id: int, db: Session = Depends(get_db)):
    db_refugee = crud.get_refugees_by_id(db, id=id)
    if db_refugee is None:
        raise HTTPException(status_code=404, detail="Refugee not found")
    return db_refugee
path += "id/"

# By family name
@router.get(
    path + "{family_name}",
    response_model=List[schemas.Refugee],
    summary="get refugee by family name",
)
def read_refugee_family_name(family_name: str, db: Session = Depends(get_db)):
    db_refugee = crud.get_refugees_by_family_name(db, family_name=family_name)
    if db_refugee is None:
        raise HTTPException(status_code=404, detail="Refugee not found")
    return db_refugee
path += "family_name/"

# By first name
@router.get(
    path + "{first_name}",
    response_model=List[schemas.Refugee],
    summary="get refugee by first name",
)
def read_refugee_first_name(first_name: str, db: Session = Depends(get_db)):
    db_refugee = crud.get_refugees_by_first_name(db, first_name=first_name)
    if db_refugee is None:
        raise HTTPException(status_code=404, detail="Refugee not found")
    return db_refugee
path += "first_name/"

# Combining family and first name
@router.get(
    path + "{family_name}/{first_name}",
    response_model=List[schemas.Refugee],
    summary="get refugee by first name and family name combination",
)
def read_refugee_first_and_family_names(first_name: str, family_name: str, db: Session = Depends(get_db)):
    db_ts = crud.get_refugees_by_first_and_family_name(db, first_name=first_name, family_name=family_name)
    if db_ts is None:
        raise HTTPException(
            status_code=404, detail="First name and Family name combination not found"
        )
    return db_ts
path += "family_name/first_name/"

# By birth date
@router.get(
    path + "{birth_date}",
    response_model=List[schemas.Refugee],
    summary="get refugee by birth date",
)
def read_refugee_birth_date(birth_date: date, db: Session = Depends(get_db)):
    db_refugee = crud.get_refugees_by_birth_date(db, birth_date=birth_date)
    if db_refugee is None:
        raise HTTPException(status_code=404, detail="Refugee not found")
    return db_refugee
path += "birth_date/"

# By salary targeted
@router.get(
    path + "{salary}",
    response_model=List[schemas.Refugee],
    summary="get refugee by salary targeted",
)
def read_refugee_salary(salary: int, db: Session = Depends(get_db)):
    db_refugee = crud.get_refugees_by_salary(db, salary=salary)
    if db_refugee is None:
        raise HTTPException(status_code=404, detail="Refugee not found")
    return db_refugee
path += "salary/"

# By Keyword
@router.get(
    path + "{keyword}",
    response_model=List[schemas.Refugee],
    summary="get refugee by keyword",
)
def read_refugee_keyword(keyword: str, db: Session = Depends(get_db)):
    db_refugee = crud.get_refugees_by_keyword(db, keyword=keyword)
    if db_refugee is None:
        raise HTTPException(status_code=404, detail="Refugee not found")
    return db_refugee
path += "keyword/"

