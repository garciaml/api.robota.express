from fastapi import APIRouter, Depends, HTTPException, Query
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
def create_refugee(refugee: schemas.RefugeeCreate, db: Session = Depends(get_db)):
    db_user = crud.get_refugees_by_attributes(db, {"email":refugee.email})
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # test if each keyword in equikeywords
    # for keyword in refugee.keywords:
    #     db_equikeyword = crud.get_equikeywords_by_attributes(db, {"label": keyword})
    #     if db_equikeyword is None:
            # if not ,
            # verify many possibilities: 
            # - changing the case (uppercase, lowercase, firt letter in uppercase, the rest in lowercase)
            # - translating into english (via google traduction with automatic detection of language)
            # - other test ? 
            # create it in equikeywords with or without generic keyword (according to previous tests)
            # crud.create_equikeyword(db=db, equikeyword={"label": keyword, "keyword": None, "refugee_id": [refugee.id]})
            # crud.create_equikeyword(db=db, equikeyword={"label": keyword, "keyword": ""})
        # else:
        #     crud.update_equikeyword_by_attributes(db=db, equikeyword={"label": keyword, "refugee_id": [refugee.id]})
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
    summary="get refugee looking by first name, family name, birth_date, salary, keyword, or just show a list of refugees between the number skip (by default None) to the number limit (by default None)",
)
# def read_refugee(first_name: Optional[str] = None, family_name: Optional[str] = None, 
#                 email: Optional[str] = None, birth_date: Optional[date] = None, 
#                 salary_targeted: Optional[int] = None, keywords: Optional[List[str]] = None, 
#                 skip: Optional[int] = 0, limit: Optional[int] = 100, db: Session = Depends(get_db)): 
def read_refugee(first_name: Optional[str] = None, family_name: Optional[str] = None, 
                email: Optional[str] = None, birth_date: Optional[date] = None, 
                salary_targeted: Optional[int] = None, keywords: Optional[List[str]] = Query(None), 
                skip: Optional[int] = None, limit: Optional[int] = None, db: Session = Depends(get_db)):  
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
        # attributes["keywords"] = []
        # # test if each keyword in equikeywords
        # for keyword in keywords:
        #     # db_equikeyword = crud.get_equikeywords_by_attributes(db, {"label": keyword})
        #     # if db_equikeyword is None:
        #     #     # if not ,
        #     #     # verify many possibilities: 
        #     #     # - changing the case (uppercase, lowercase, firt letter in uppercase, the rest in lowercase)
        #     #     # - translating into english (via google traduction with automatic detection of language)
        #     #     # - other test ? 
        #     #     # create it in equikeywords with or without generic keyword (according to previous tests)
        #     #     crud.create_equikeyword(db=db, equikeyword={"label": keyword, "keyword": None, "refugee_id": })
        #     # add keywords to attributes
        #     attributes["keywords"].append(keyword)
    db_ts = crud.get_refugees_by_attributes(db, attributes)
    # if db_ts is None:
    #     raise HTTPException(
    #         status_code=404, detail="Refugee not found"
    #     )
    if db_ts is None:
        db_refugee = crud.get_refugees(db, skip=skip, limit=limit)
        if db_refugee is None:
            raise HTTPException(status_code=404, detail="Refugees not found")
        else:
            return db_refugee
    else:
        return db_ts
