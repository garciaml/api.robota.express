from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy.sql import or_, and_

from . import models, schemas

import unidecode

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
# - case there is equikeyword existing but in another language when creating refugee
# - for get by keywords, look for equivalent keywords thanks to the generic keywords (in order to find more people who may talk different language)
#
# 


### Refugees: 
# CREATE
def create_refugee(db: Session, refugee: schemas.RefugeeCreate): # maybe put a keywords_id to link with equivalence table ?
    new_refugee = refugee.dict()
    new_refugee["keywords"] = []
    # db_refugee = models.Refugee(**refugee.dict())
    db_refugee = models.Refugee(**new_refugee)
    for k in refugee.dict()['keywords']:
        if db.get(models.EquivalentKeyword, k) is None:
            new_equikeyword = generate_new_equikeyword_when_no_existing(db, k)
            if new_equikeyword:
                create_equikeyword(db, new_equikeyword)
            else:
                # no generic keyword found
                create_equikeyword(db, {"label": k}) 
        db_equikeyword = db.get(models.EquivalentKeyword, k)
        # db_equikeyword = db.get(models.EquivalentKeyword, k)
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
    # BE CAREFUL: it fully replaces keywords by new values; 
    # if you want to add or delete certain values, create your list of keywords accordingly.
    if refugee.dict()['keywords']:
        new_refugee["keywords"] = []
        for k in refugee.dict()['keywords']:
            if db.get(models.EquivalentKeyword, k) is None:
                new_equikeyword = generate_new_equikeyword_when_no_existing(db, k)
                if new_equikeyword:
                    create_equikeyword(db, new_equikeyword)
                else:
                    # no generic keyword found
                    create_equikeyword(db, {"label": k})
            db_equikeyword = db.get(models.EquivalentKeyword, k)
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



### EquivalentKeywords:
# CREATE
def create_equikeyword(db: Session, equikeyword: schemas.EquivalentKeyword):
    db_equikeyword = models.EquivalentKeyword(**equikeyword)
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

# DELETE
def delete_equikeyword(db: Session, label: str):
    db_equikeyword = db.get(models.EquivalentKeyword, label)
    db.delete(db_equikeyword)
    db.commit()
    return True

def generate_new_equikeyword_when_no_existing(db: Session, keyword: str):
    new_equikeyword = None
    # first, we need to test if we can find a generic keyword
    if db.get(models.Keyword, keyword):
        new_equikeyword = {"label": keyword, "keyword": keyword}
    # remove accent
    unaccented_string = unidecode.unidecode(keyword)
    unaccented_string_lower = unaccented_string.lower()
    unaccented_string_upper = unaccented_string.upper()
    unaccented_string_capital = unaccented_string.capitalize()
    if db.get(models.EquivalentKeyword, unaccented_string):
        db_equikeyword_other = db.get(models.EquivalentKeyword, unaccented_string)
        new_equikeyword = {"label": keyword, "keyword": db_equikeyword_other.keyword}
    elif db.get(models.Keyword, unaccented_string):
        new_equikeyword = {"label": keyword, "keyword": unaccented_string}
    elif db.get(models.EquivalentKeyword, unaccented_string_lower):
        db_equikeyword_other = db.get(models.EquivalentKeyword, unaccented_string_lower)
        new_equikeyword = {"label": keyword, "keyword": db_equikeyword_other.keyword}
    elif db.get(models.Keyword, unaccented_string_lower):
        new_equikeyword = {"label": keyword, "keyword": unaccented_string_lower}
    elif db.get(models.EquivalentKeyword, unaccented_string_upper):
        db_equikeyword_other = db.get(models.EquivalentKeyword, unaccented_string_upper)
        new_equikeyword = {"label": keyword, "keyword": db_equikeyword_other.keyword}
    elif db.get(models.Keyword, unaccented_string_upper):
        new_equikeyword = {"label": keyword, "keyword": unaccented_string_upper}
    elif db.get(models.EquivalentKeyword, unaccented_string_capital):
        db_equikeyword_other = db.get(models.EquivalentKeyword, unaccented_string_capital)
        new_equikeyword = {"label": keyword, "keyword": db_equikeyword_other.keyword}
    elif db.get(models.Keyword, unaccented_string_capital):
        new_equikeyword = {"label": keyword, "keyword": unaccented_string_capital}
    # transform the case
    # capitalize and verify in the table Keyword
    capital_k = keyword.capitalize()
    if db.get(models.EquivalentKeyword, capital_k):
        db_equikeyword_other = db.get(models.EquivalentKeyword, capital_k)
        new_equikeyword = {"label": keyword, "keyword": db_equikeyword_other.keyword}
    elif db.get(models.Keyword, capital_k):
        new_equikeyword = {"label": keyword, "keyword": capital_k}
    # lower and verify in EquivalentKeyword
    lower_k = keyword.lower()
    if db.get(models.EquivalentKeyword, lower_k):
        db_equikeyword_other = db.get(models.EquivalentKeyword, lower_k)
        new_equikeyword = {"label": keyword, "keyword": db_equikeyword_other.keyword}
    elif db.get(models.Keyword, lower_k):
        new_equikeyword = {"label": keyword, "keyword": lower_k}
    # upper and verify in EquivalentKeyword
    upper_k = keyword.upper()
    if db.get(models.EquivalentKeyword, upper_k):
        db_equikeyword_other = db.get(models.EquivalentKeyword, upper_k)
        new_equikeyword = {"label": keyword, "keyword": db_equikeyword_other.keyword}
    elif db.get(models.Keyword, upper_k):
        new_equikeyword = {"label": keyword, "keyword": upper_k}
    return new_equikeyword


### Keywords: 
# CREATE
def create_keyword(db: Session, keyword: schemas.Keyword):
    db_keyword = models.Keyword(**keyword)
    db.add(db_keyword)
    db.commit()
    db.refresh(db_keyword)
    return db_keyword

# READ
def get_keywords(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Keyword).offset(skip).limit(limit).all()

def get_keywords_by_label(db: Session, label: str):
    return db.get(models.Keyword, label)

# UPDATE
def update_keyword(db: Session, keyword: schemas.KeywordUpdate):
    # get the existing data
    db_keyword = db.query(models.Keyword).filter(models.Keyword.label == keyword.label).one_or_none()
    setattr(db_keyword, 'label',  keyword.new_label)
    # db_keyword.update({'label': keyword.new_label})
    # make updates directly saved and visible in the database
    db.commit()
    db.refresh(db_keyword)
    # TODO: get equikeyword by keyword, update keyword 
    # get the existing data
    db_equikeyword = db.query(models.EquivalentKeyword).filter(models.EquivalentKeyword.keyword == keyword.label).all()
    # update the fields to update
    for db_equikeyword_one in db_equikeyword: 
        setattr(db_equikeyword_one, 'keyword', keyword.new_label)
        # make updates directly saved and visible in the database
        db.commit()
        db.refresh(db_equikeyword_one)
    return db_keyword

# DELETE
def delete_keyword(db: Session, label: str):
    db_keyword = db.get(models.Keyword, label)
    db.delete(db_keyword)
    db.commit()
    return True


# Employers

