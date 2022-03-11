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
                salary: Optional[int] = None, keyword: Optional[str] = None, db: Session = Depends(get_db)):  
    if first_name:
        # First name
        if (family_name is None) & (email is None) & (birth_date is None) & (salary is None) & (keyword is None):
            db_ts = crud.get_refugees_by_first_name(db, first_name=first_name)
            if db_ts is None:
                raise HTTPException(
                    status_code=404, detail="First name not found"
                )
        # First name + Family name
        elif (family_name is not None) & (email is None) & (birth_date is None) & (salary is None) & (keyword is None):
            db_ts = crud.get_refugees_by_first_and_family_name(db, first_name=first_name, family_name=family_name)
        # First name + email
        elif (family_name is None) & (email is not None) & (birth_date is None) & (salary is None) & (keyword is None):
            db_ts = crud.get_refugees_by_first_name_and_email()
        # First name + Family name + email
        elif (family_name is not None) & (email is not None) & (birth_date is None) & (salary is None) & (keyword is None):
            db_ts = crud.get_refugees_by_first_and_family_name_and_email(db, first_name=first_name, family_name=family_name, email=email)
        # First name + Family name + email + birth date
        elif (family_name is not None) & (email is not None) & (birth_date is not None) & (salary is None) & (keyword is None):
            db_ts = crud.get_refugees_by_first_and_family_name_and_email_and_birth_date(db, first_name=first_name, family_name=family_name, email=email, birth_date=birth_date)
        # First name + Family name + email + birth date + salary
        elif (family_name is not None) & (email is not None) & (birth_date is not None) & (salary is not None) & (keyword is None):
            db_ts = crud.get_refugees_by_first_and_family_name_and_email_and_birth_date_and_salary(db, first_name=first_name, family_name=family_name, email=email, birth_date=birth_date, salary=salary)
        # First name + Family name + email + birth date + salary + keyword
        elif (family_name is not None) & (email is not None) & (birth_date is not None) & (salary is not None) & (keyword is not None):
            db_ts = crud.get_refugees_by_first_and_family_name_and_email_and_birth_date_and_salary_and_keyword(db, first_name=first_name, family_name=family_name, email=email, birth_date=birth_date, salary=salary, keyword=keyword)
    
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

