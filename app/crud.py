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
    # return [attributes]
    return db.query(models.Refugee).filter_by(**attributes).all()
    # for attribute in dict:
    #     print(attribute, dict[attribute])
    # return db.query(models.Refugee).filter_by(attribute == dict[attribute] for attribute in dict if dict[attribute] is not None).all()
    # db_query = db.query(models.Refugee)
    # for attribute in dict:
    #     if dict[attribute] is not None:
    #         db_query.filter_by(attribute == dict[attribute])
    # return db_query.all()
    # attributes = []
    # values = []
    # for attribute in list(dict.keys()):
    #     if dict[attribute] is not None:
    #         attributes.append(attribute)
    #         values.append(dict[attribute])
    
    # if len(attributes) == 1:
    #     att0 = attributes[0]
    #     val0 = values[0]
    #     return db.query(models.Refugee).filter_by(att0.like(val0)).all()
    # elif len(attributes) == 2:
    #     return db.query(models.Refugee).filter_by(attributes[0] == values[0], attributes[1] == values[1]).all()
    # elif len(attributes) == 3:
    #     return db.query(models.Refugee).filter_by(attributes[0] == values[0], attributes[1] == values[1], attributes[2] == values[2]).all()
    # elif len(attributes) == 4:
    #     return (
    #         db.query(models.Refugee).filter_by(attributes[0] == values[0], 
    #                                        attributes[1] == values[1], 
    #                                        attributes[2] == values[2],
    #                                        attributes[3] == values[3]).all()
    #                                        )
    # elif len(attributes) == 5:
    #     return (
    #         db.query(models.Refugee).filter_by(attributes[0] == values[0], 
    #                                        attributes[1] == values[1], 
    #                                        attributes[2] == values[2],
    #                                        attributes[3] == values[3],
    #                                        attributes[4] == values[4]).all()
    #                                        )
    # elif len(attributes) == 6:
    #     return (
    #         db.query(models.Refugee).filter_by(attributes[0] == values[0], 
    #                                        attributes[1] == values[1], 
    #                                        attributes[2] == values[2],
    #                                        attributes[3] == values[3],
    #                                        attributes[4] == values[4],
    #                                        attributes[5] == values[5]).all()
    #                                        )


# def get_refugees_by_family_name(db: Session, family_name: str):
#     return db.query(models.Refugee).filter(models.Refugee.family_name.like(family_name+"%")).all() # add the "%" to show all the names starting by family_name

# def get_refugees_by_first_name(db: Session, first_name: str):
#     return db.query(models.Refugee).filter(models.Refugee.first_name.like(first_name)).all()

# def get_refugees_by_first_and_family_name(db: Session, first_name: str, family_name: str):
#     return (
#         db.query(models.Refugee)
#         .filter(models.Refugee.first_name.like(first_name), models.Refugee.family_name.like(family_name))
#         .all()
#     )
# def get_refugees_by_birth_date(db: Session, birth_date: date):
#     return db.query(models.Refugee).filter(models.Refugee.birth_date == birth_date).all()

# def get_refugees_by_salary(db: Session, salary: int = 0):
#     return db.query(models.Refugee).filter(models.Refugee.salary_targeted == salary).all()

# def get_refugees_by_email(db: Session, email: str):
#     return db.query(models.Refugee).filter(models.Refugee.email == email).first()

# def get_refugees_by_keyword(db: Session, keyword: str):
#     return (
#         db.query(models.Refugee, models.Keyword, models.EquivalentKeyword)
#         .filter(models.Refugee.keyword.contains(models.EquivalentKeyword.keyword))
#         .filter(models.EquivalentKeyword.keyword == models.Keyword.label)
#         .filter(models.Keyword.label == keyword)
#         .all()
#     )
# def get_refugees_by_keyword(db: Session, keyword: str):
#     return (
#         db.query(models.EquivalentKeyword)
#         .filter(models.EquivalentKeyword.keyword.contains(keyword))
#         .all()
#     )

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

