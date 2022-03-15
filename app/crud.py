from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy.sql import or_, and_

from . import models, schemas

# HELP: see https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_filter_operators.htm
# --> use IN for Keywords (split text by comma, and use the list as a paam to the ".in" method)

# get refugee by keywords:
# https://stackoverflow.com/questions/14534321/how-can-i-search-the-table-of-a-flask-sqlalchemy-many-to-many-relationship


# Refugees: 
# CREATE
def create_refugee(db: Session, refugee: schemas.RefugeeCreate): # maybe put a keywords_id to link with equivalence table ?
    new_refugee = refugee.dict()
    new_refugee["keywords"] = []
    # db_refugee = models.Refugee(**refugee.dict())
    db_refugee = models.Refugee(**new_refugee)
    for k in refugee.dict()['keywords']:
        # db_equikeyword = db.get(models.EquivalentKeyword, k)
        # if db_equikeyword is None:
        #     create_equikeyword(db, {"label": k}) # TODOs: add other tests to see if we can put a generic keyword 
        #     db_equikeyword = db.get(models.EquivalentKeyword, k)
        db_equikeyword = db.query(models.EquivalentKeyword).filter_by(label=k).first()
        db_refugee.keywords.append(
            db_equikeyword
            # db.get(models.EquivalentKeyword, k)
            # db.query(models.EquivalentKeyword).filter_by(label=k)
        )
        # db_refugee.keywords.append(k)
    db.add(db_refugee)
    db.commit()
    db.refresh(db_refugee)
    return db_refugee

# READ
def get_refugees(db: Session, skip: int = 0, limit: int = 100):
    #return db.get(models.Refugee, refugee)
    return db.query(models.Refugee).offset(skip).limit(limit).all()

def get_refugees_by_id(db: Session, id: int = 0):
    # return db.query(models.Refugee).filter(models.Refugee.id == id).all()
    return db.get(models.Refugee, id)

def get_refugees_by_attributes(db: Session, attributes):
    # keyword = attributes["keywords"]
    # del attributes["keywords"]
    # and next maybe add a filter to put filter(models.Refugee.keywords.contains(keywords))
    return db.query(models.Refugee).filter_by(**attributes).all()

def get_refugees_by_keywords_and_attributes(db: Session, keywords, attributes, inclusive: bool = True):
    cond = or_(*[models.EquivalentKeyword.label == keyword for keyword in keywords]) 
    equikeywords = db.query(models.EquivalentKeyword).filter(cond)
    if inclusive:
        cond = or_(*[models.Refugee.keywords.contains(keyword) for keyword in equikeywords])
    else:
        cond = and_(*[models.Refugee.keywords.contains(keyword) for keyword in equikeywords]) 
    return db.query(models.Refugee).filter(cond).filter_by(**attributes).all()

def get_refugees_by_keywords(db: Session, keywords, inclusive: bool = True):
    # return [db.query(models.EquivalentKeyword).filter(models.EquivalentKeyword.label.in_(keywords)).label("refugee_id")]
    cond = or_(*[models.EquivalentKeyword.label == keyword for keyword in keywords]) 
    equikeywords = db.query(models.EquivalentKeyword).filter(cond)
    if inclusive:
        cond = or_(*[models.Refugee.keywords.contains(keyword) for keyword in equikeywords])
    else:
        cond = and_(*[models.Refugee.keywords.contains(keyword) for keyword in equikeywords]) 
    return db.query(models.Refugee).filter(cond).all()

# EquivalentKeywords:
# CREATE
def create_equikeyword(db: Session, equikeyword: schemas.EquivalentKeyword):
    db_equikeyword = models.EquivalentKeyword(**equikeyword.dict())
    db.add(db_equikeyword)
    db.commit()
    db.refresh(db_equikeyword)
    return db_equikeyword

# READ
def get_equikeywords_by_label(db: Session, label: str):
    return db.query(models.EquivalentKeyword).filter(models.EquivalentKeyword.label == label).first()

def get_equikeywords_by_attributes(db: Session, attributes):
    return db.query(models.EquivalentKeyword).filter_by(**attributes).all()

# UPDATE
def update_equikeyword_refugee(db: Session, attributes):
    return db.query(models.EquivalentKeyword).filter(models.EquivalentKeyword.label == attributes['label']).update({"refugee_id": (models.EquivalentKeyword.refugee_id + attributes['refugee_id'])})
#def update_equikeyword_keyword(db: Session, attributes):


# Keywords: CREATE
def create_keyword(db: Session, keyword: schemas.Keyword):
    db_keyword = models.Keyword(**keyword.dict())
    db.add(db_keyword)
    db.commit()
    db.refresh(db_keyword)
    return db_keyword

def get_keywords_by_label(db: Session, label: str):
    return db.query(models.Keyword).filter(models.Keyword.label.like(label)).first()



# Employers

