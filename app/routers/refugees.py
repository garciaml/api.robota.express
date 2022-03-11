from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, engine
from typing import List, Optional
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
# By identifier
@router.get(
    "/{id}",
    response_model=schemas.Refugee,
    summary="get refugee by identifier",
)
def read_refugee_id(id: int, db: Session = Depends(get_db)):
    db_refugee = crud.get_refugees_by_id(db, id=id)
    if db_refugee is None:
        raise HTTPException(status_code=404, detail="Refugee not found")
    return db_refugee

# By other parameters
@router.get(
    "/",
    response_model=List[schemas.Refugee],
    summary="get refugee looking by first name, family name, birth_date, salary, keyword",
)
def read_refugee(first_name: Optional[str] = None, family_name: Optional[str] = None, 
                email: Optional[str] = None, birth_date: Optional[date] = None, 
                salary_targeted: Optional[int] = None, keywords: Optional[str] = None, db: Session = Depends(get_db)):  
    attributes = {}
    if first_name:
        attributes["first_name"] = first_name
    if family_name:
        attributes["family_name"] = family_name
    if email:
        attributes["email"] = email
    if birth_date:
        attributes["birth_date"] = birth_date
    if salary_targeted:
        attributes["salary_targeted"] = salary_targeted
    if keywords:
        attributes["keywords"] = keywords
    # db_ts = crud.get_refugees_by_attributes(db, first_name=first_name, family_name=family_name, 
    #             email=email, birth_date=birth_date, 
    #             salary_targeted=salary_targeted, keywords=keywords)
    db_ts = crud.get_refugees_by_attributes(db, attributes)
    if db_ts is None:
        raise HTTPException(
            status_code=404, detail="First name not found"
        )
    return db_ts




    
    
# # By family name
# @router.get(
#     "/",
#     response_model=List[schemas.Refugee],
#     summary="get refugee by family name",
# )
# def read_refugee_params(family_name: str, db: Session = Depends(get_db)):
#     db_refugee = crud.get_refugees_by_family_name(db, family_name=family_name)
#     if db_refugee is None:
#         raise HTTPException(status_code=404, detail="Refugee not found")
#     return db_refugee
# path += "family_name/"

# # By first name
# @router.get(
#     "/",
#     response_model=List[schemas.Refugee],
#     summary="get refugee by first name",
# )
# def read_refugee_first_name(first_name: str, db: Session = Depends(get_db)):
#     db_refugee = crud.get_refugees_by_first_name(db, first_name=first_name)
#     if db_refugee is None:
#         raise HTTPException(status_code=404, detail="Refugee not found")
#     return db_refugee

# By birth date
# @router.get(
#     path + "{birth_date}",
#     response_model=List[schemas.Refugee],
#     summary="get refugee by birth date",
# )
# def read_refugee_birth_date(birth_date: date, db: Session = Depends(get_db)):
#     db_refugee = crud.get_refugees_by_birth_date(db, birth_date=birth_date)
#     if db_refugee is None:
#         raise HTTPException(status_code=404, detail="Refugee not found")
#     return db_refugee

# By salary targeted
# @router.get(
#     path + "{salary}",
#     response_model=List[schemas.Refugee],
#     summary="get refugee by salary targeted",
# )
# def read_refugee_salary(salary: int, db: Session = Depends(get_db)):
#     db_refugee = crud.get_refugees_by_salary(db, salary=salary)
#     if db_refugee is None:
#         raise HTTPException(status_code=404, detail="Refugee not found")
#     return db_refugee

# By Keyword
# @router.get(
#     path + "{keyword}",
#     response_model=List[schemas.Refugee],
#     summary="get refugee by keyword",
# )
# def read_refugee_keyword(keyword: str, db: Session = Depends(get_db)):
#     db_refugee = crud.get_refugees_by_keyword(db, keyword=keyword)
#     if db_refugee is None:
#         raise HTTPException(status_code=404, detail="Refugee not found")
#     return db_refugee

