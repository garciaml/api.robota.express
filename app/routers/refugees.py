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
    # The dictionary "attributes" must not contain None values 
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
    db_ts = crud.get_refugees_by_attributes(db, attributes)
    if db_ts is None:
        raise HTTPException(
            status_code=404, detail="Refugee not found"
        )
    return db_ts
