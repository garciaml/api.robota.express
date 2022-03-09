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

# By identifier
@router.get(
    "?id_refugee={id_refugee}",
    response_model=List[schemas.Refugee],
    summary="get refugee by identifier",
)
def read_refugee_id(id_refugee: int, db: Session = Depends(get_db)):
    db_refugee = crud.get_refugees_by_id(db, id=id_refugee)
    if db_refugee is None:
        raise HTTPException(status_code=404, detail="Refugee not found")
    return db_refugee

# By family name
@router.get(
    "?family_name={family_name}",
    response_model=List[schemas.Refugee],
    summary="get refugee by family name",
)
def read_refugee_family_name(family_name: str, db: Session = Depends(get_db)):
    db_refugee = crud.get_refugees_by_family_name(db, family_name=family_name)
    if db_refugee is None:
        raise HTTPException(status_code=404, detail="Refugee not found")
    return db_refugee

# By first name
@router.get(
    "?first_name={first_name}",
    response_model=List[schemas.Refugee],
    summary="get refugee by first name",
)
def read_refugee_first_name(first_name: str, db: Session = Depends(get_db)):
    db_refugee = crud.get_refugees_by_first_name(db, first_name=first_name)
    if db_refugee is None:
        raise HTTPException(status_code=404, detail="Refugee not found")
    return db_refugee

# Combining family and first name
@router.get(
    "?first_name={first_name}&family_name={family_name}",
    response_model=List[schemas.Refugee],
    summary="get refugee by first name and family name combination",
)
def read_refugee_first_and_family_names(first_name: str, family_name: str, db: Session = Depends(get_db)):
    db_ts = crud.get_points_by_team_and_season(db, first_name=first_name, family_name=family_name)
    if db_ts is None:
        raise HTTPException(
            status_code=404, detail="First name and Family name combination not found"
        )
    return db_ts

# By birth date
@router.get(
    "?birth_date={birth_date}",
    response_model=List[schemas.Refugee],
    summary="get refugee by birth date",
)
def read_refugee_birth_date(birth_date: date, db: Session = Depends(get_db)):
    db_refugee = crud.get_refugees_by_birth_date(db, birth_date=birth_date)
    if db_refugee is None:
        raise HTTPException(status_code=404, detail="Refugee not found")
    return db_refugee

# By salary targeted
@router.get(
    "?salary={salary}",
    response_model=List[schemas.Refugee],
    summary="get refugee by salary targeted",
)
def read_refugee_salary(salary: int, db: Session = Depends(get_db)):
    db_refugee = crud.get_refugees_by_salary(db, salary=salary)
    if db_refugee is None:
        raise HTTPException(status_code=404, detail="Refugee not found")
    return db_refugee

# By Keyword
@router.get(
    "?keyword={keyword}",
    response_model=List[schemas.Refugee],
    summary="get refugee by keyword",
)
def read_refugee_keyword(keyword: str, db: Session = Depends(get_db)):
    db_refugee = crud.get_refugees_by_keyword(db, keyword=keyword)
    if db_refugee is None:
        raise HTTPException(status_code=404, detail="Refugee not found")
    return db_refugee