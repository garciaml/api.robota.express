from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy.sql import or_, and_

from . import models, schemas

# HELP: see https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_filter_operators.htm
# --> use IN for Keywords (split text by comma, and use the list as a paam to the ".in" method)

# get refugee by keywords:
# https://stackoverflow.com/questions/14534321/how-can-i-search-the-table-of-a-flask-sqlalchemy-many-to-many-relationship

# comparison between commit, flush, expire, refresh, and merge
#  https://michaelcho.me/article/sqlalchemy-commit-flush-expire-refresh-merge-whats-the-difference 

# update: https://stackoverflow.com/questions/63143731/update-sqlalchemy-orm-existing-model-from-posted-pydantic-model-in-fastapi
# https://github.com/mikey-no/pydantic-sqlalchemy-experiments/blob/main/main.py

# several ways to update + count number of logins of users
# https://stackoverflow.com/questions/9667138/how-to-update-sqlalchemy-row-entry 

# TODO:
# - case there is no equikeyword existing when creating refugee
# - delete by id
# - for get by keywords, look for equivalent keywords thanks to the generic keywords (in order to find more people who may talk different language)

### Refugees: 
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
    db.add(db_refugee)
    db.commit()
    db.refresh(db_refugee)
    return db_refugee

# READ
def get_refugees(db: Session, skip: int = 0, limit: int = 100):
    #return db.get(models.Refugee, refugee)
    return db.query(models.Refugee).offset(skip).limit(limit).all()

def get_refugees_by_id(db: Session, id: int = 0):
    return db.get(models.Refugee, id)

def get_refugees_by_attributes(db: Session, attributes):
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
    cond = or_(*[models.EquivalentKeyword.label == keyword for keyword in keywords]) 
    equikeywords = db.query(models.EquivalentKeyword).filter(cond)
    if inclusive:
        cond = or_(*[models.Refugee.keywords.contains(keyword) for keyword in equikeywords])
    else:
        cond = and_(*[models.Refugee.keywords.contains(keyword) for keyword in equikeywords]) 
    return db.query(models.Refugee).filter(cond).all()

# UPDATE
def update_refugees(db: Session, refugee: schemas.RefugeeUpdate):
    # get the existing data
    db_refugee = db.query(models.Refugee).filter(models.Refugee.id == refugee.id).one_or_none()
    # we keep only the fields that are not empty
    new_refugee = {}
    for k in refugee.dict().keys():
        if refugee.dict()[k]:
            new_refugee[k] = refugee.dict()[k]
    # we need items of models.EquivalentKeyword
    if refugee.dict()['keywords']:
        new_refugee["keywords"] = []
        for k in refugee.dict()['keywords']:
            # db_equikeyword = db.get(models.EquivalentKeyword, k)
            # if db_equikeyword is None:
            #     create_equikeyword(db, {"label": k}) # TODO: add other tests to see if we can put a generic keyword 
            #     db_equikeyword = db.get(models.EquivalentKeyword, k)
            db_equikeyword = db.query(models.EquivalentKeyword).filter_by(label=k).first()
            new_refugee["keywords"].append(db_equikeyword)
    # update the fields to update
    for var, value in new_refugee.items(): setattr(db_refugee, var, value)
    # make updates directly saved and visible in the database
    db.commit()
    db.refresh(db_refugee)
    return db_refugee

# DELETE
def delete_refugees(db: Session, id: int):
    db_refugee = db.get(models.Refugee, id)
    db.delete(db_refugee)
    db.commit()
    return True


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

