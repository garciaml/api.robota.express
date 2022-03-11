from sqlalchemy.orm import Session
from datetime import date

from . import models, schemas

# HELP: see https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_filter_operators.htm
# --> use IN for Keywords (split text by comma, and use the list as a paam to the ".in" method)
# Refugees: READ
def get_refugees(db: Session, skip: int = 0, limit: int = 100):
    #return db.get(models.Refugee, refugee)
    return db.query(models.Refugee).offset(skip).limit(limit).all()

def get_refugees_by_id(db: Session, id: int = 0):
    # return db.query(models.Refugee).filter(models.Refugee.id == id).all()
    return db.get(models.Refugee, id)

def get_refugees_by_attributes(db: Session, attributes):
    return db.query(models.Refugee).filter_by(**attributes).all()

# Refugees: CREATE
def create_refugee(db: Session, refugee: schemas.Refugee): # maybe put a keywords_id to link with equivalence table ? 
    db_refugee = models.Refugee(**refugee.dict())
    db.add(db_refugee)
    db.commit()
    db.refresh(db_refugee)
    return db_refugee


# Keywords: CREATE
# def get_equikeywords_by_keyword(db: Session, keyword: str):
def create_keyword(db: Session, keyword: schemas.Keyword): 
    db_keyword = models.Keyword(**keyword.dict())
    db.add(db_keyword)
    db.commit()
    db.refresh(db_keyword)
    return db_keyword

def get_keywords_by_label(db: Session, label: str):
    return db.query(models.Keyword).filter(models.Keyword.label.like(label)).first()

# EquivalentKeywords: CREATE
def create_equikeyword(db: Session, equikeyword: schemas.EquivalentKeyword): 
    db_equikeyword = models.EquivalentKeyword(**equikeyword.dict())
    db.add(db_equikeyword)
    db.commit()
    db.refresh(db_equikeyword)
    return db_equikeyword

def get_equikeywords_by_label(db: Session, label: str):
    return db.query(models.EquivalentKeyword).filter(models.EquivalentKeyword.label == label).first()

def get_equikeywords_by_keyword(db: Session, keyword: str):
    return db.query(models.EquivalentKeyword).filter(models.EquivalentKeyword.keyword == keyword).all()

# Employers

