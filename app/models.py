from unicodedata import category
from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String, Date, Float, Text
from sqlalchemy.orm import relationship

from .database import Base

# TODO:
# - for Refugee, create keywords (that people can tick, sorted by category)
# - for Refugee, create new_keywords (that people can write, to be analysed and placed in the table Keyword)
# - create table Employer
# - create table Organization
# - create table JobOffer
# - create table Trainer
# - create table TrainingCategory (categories of training, linguage, etc.)
# - create table TrainingOffer (an offer of training, learn French, etc.)
# - create table Funder
# - generate id automatically (rm from schemas and in function create add random id)
# - look for uppercase/lowercase/capital names when looking for name OR save names in uppercase ?


association_table = Table('association_refugee_equikeyword', Base.metadata,
    Column('refugee_id', ForeignKey('refugee.id')),
    Column('equikeyword_label', ForeignKey('equikeyword.label'))
    )

association_table_company_employees = Table('association_table_company_employees', Base.metadata,
    Column('company_id', ForeignKey('company.id')),
    Column('employee_id', ForeignKey('recruiter.id'))
    )

association_table_company_offers = Table('association_table_company_offers', Base.metadata,
    Column('company_id', ForeignKey('company.id')),
    Column('offer_id', ForeignKey('job_offer.id'))
    )

association_table_recruiters_offers = Table('association_table_recruiters_offers', Base.metadata,
    Column('recruiter_id', ForeignKey('recruiter.id')),
    Column('offer_id', ForeignKey('job_offer.id'))
    )

association_table_equikeywords_companies = Table('association_table_equikeywords_companies', Base.metadata,
    Column('equikeyword_label', ForeignKey('equikeyword.label')),
    Column('company_id', ForeignKey('company.id'))
    )

association_table_equikeywords_recruiters = Table('association_table_equikeywords_recruiters', Base.metadata,
    Column('equikeyword_label', ForeignKey('equikeyword.label')),
    Column('recruiter_id', ForeignKey('recruiter.id'))
    )

association_table_equikeywords_offers = Table('association_table_equikeywords_offers', Base.metadata,
    Column('equikeyword_label', ForeignKey('equikeyword.label')),
    Column('offer_id', ForeignKey('job_offer.id'))
    )


class Refugee(Base):
    __tablename__ = "refugee"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    family_name = Column(String(50))
    birth_date = Column(Date)
    salary_targeted = Column(Integer)
    email = Column(String(50))
    # keywords = relationship("Item", back_populates="owner")
    # keywords = Column(Text) # text of words separated by a comma (to be ordered and cleaned in the front-end part, before storing in json?)
    keywords = relationship(
        "EquivalentKeyword", 
        secondary=association_table,
        back_populates="refugee_id"
    )


class EquivalentKeyword(Base):
    __tablename__ = "equikeyword"

    label = Column(String(50), primary_key=True, index=True)
    keyword = Column(String(50), ForeignKey('keyword.label')) # IMPORTANT: when removing a Keyword, not erased here !
    refugee_id = relationship(
        "Refugee",
        secondary=association_table,
        back_populates="keywords"
    )
    company = relationship(
        "EquivalentKeyword", 
        secondary=association_table_equikeywords_companies,
        back_populates="keywords"
    )
    recruiter = relationship(
        "EquivalentKeyword", 
        secondary=association_table_equikeywords_recruiters,
        back_populates="keywords"
    )
    job_offer = relationship(
        "EquivalentKeyword", 
        secondary=association_table_equikeywords_offers,
        back_populates="keywords"
    )


class Keyword(Base):
    __tablename__ = "keyword"
    label = Column(String(50), primary_key=True, index=True)
    # category = Column(String(50))

# Company
class Company(Base):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    address = Column(String(50))
    country = Column(String(50))
    email = Column(String(50))
    phone = Column(String(50))
    employees = relationship(
        "Recruiter",
        secondary=association_table_company_employees,
        back_populates="company"
    )
    offers = relationship(
        "JobOffer",
        secondary=association_table_company_offers,
        back_populates="company"
    ) 
    keywords = relationship(
        "EquivalentKeyword", 
        secondary=association_table_equikeywords_companies,
        back_populates="company"
    )

# Employer
class Recruiter(Base):
    __tablename__ = "recruiter"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    phone = Column(String(50))
    company = relationship(
        "Company",
        secondary=association_table_company_employees,
        back_populates="employees"
    )
    offers = relationship(
        "JobOffer",
        secondary=association_table_recruiters_offers,
        back_populates="recruiters"
    )
    keywords = relationship(
        "EquivalentKeyword", 
        secondary=association_table_equikeywords_recruiters,
        back_populates="recruiter"
    )

# Job offer
class JobOffer(Base):
    __tablename__ = "job_offer"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(50))
    city = Column(String(50))
    address = Column(String(50))
    title = Column(String(50))
    link_to_description = Column(String(50)) # store raw description for low data users?
    company = relationship(
        "Company",
        secondary=association_table_company_offers,
        back_populates="offers"
    ) 
    recruiters = relationship(
        "Recruiter",
        secondary=association_table_recruiters_offers,
        back_populates="offers"
    )
    keywords = relationship(
        "EquivalentKeyword", 
        secondary=association_table_equikeywords_offers,
        back_populates="job_offer"
    )

# Training center
# Trainer
# Training offer