from typing import List, Optional
from unicodedata import category
from pydantic import BaseModel
from datetime import date


class RefugeeBase(BaseModel):
    id: int
    first_name: str
    family_name: str
    birth_date: Optional[date] = None
    salary_targeted: Optional[int] = None
    email: str

    class Config:
        orm_mode = True

class RefugeeCreate(RefugeeBase):
    # keywords: Optional[List[EquivalentKeywordBase]] = None
    keywords: Optional[List[str]] = None

    class Config:
        orm_mode = True

class RefugeeUpdate(BaseModel):
    id: int
    first_name: Optional[str] = None
    family_name: Optional[str] = None
    birth_date: Optional[date] = None
    salary_targeted: Optional[int] = None
    email: Optional[str] = None
    keywords: Optional[List[str]] = None

    class Config:
        orm_mode = True

class EquivalentKeywordBase(BaseModel):
# class EquivalentKeyword(BaseModel):
    label: str
    keyword: Optional[str] = None
    # refugee_id: Optional[List[int]] = None

    class Config:
        orm_mode = True

class EquivalentKeywordCreate(EquivalentKeywordBase):
    # refugee_id: Optional[List[RefugeeBase]] = None
    refugee_id: Optional[List[str]] = None

class Refugee(RefugeeBase):
    keywords: Optional[List[EquivalentKeywordBase]] = None
    # keywords: Optional[List[str]] = None

    class Config:
        orm_mode = True

class EquivalentKeyword(EquivalentKeywordBase):
    refugee_id: Optional[List[RefugeeBase]] = None
    # refugee_id: Optional[List[str]]

    class Config:
        orm_mode = True

class Keyword(BaseModel):
    label: str
    # category: Optional[str]

    class Config:
        orm_mode = True

class KeywordUpdate(BaseModel):
    label: str
    new_label: str
    # category: Optional[str]

    class Config:
        orm_mode = True

class CompanyBase(BaseModel):
    id: int
    name: str
    country: str
    address: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        orm_mode = True


class Company(CompanyBase):
    keywords: Optional[List[str]] = None
    # offers: Optional[List[str]] = None
    # employees: Optional[List[str]] = None

    class Config:
        orm_mode = True

class CompanyUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    keywords: Optional[List[str]] = None
    offers: Optional[List[str]] = None
    employees: Optional[List[str]] = None

    class Config:
        orm_mode = True


class RecruiterBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None

    class Config:
        orm_mode = True

class Recruiter(RecruiterBase):
    keywords: Optional[List[str]] = None
    offers: Optional[List[str]] = None
    company: Optional[List[str]] = None

    class Config:
        orm_mode = True

class RecruiterUpdate(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    keywords: Optional[List[str]] = None
    offers: Optional[List[str]] = None
    company: Optional[List[str]] = None

    class Config:
        orm_mode = True


class JobOfferBase(BaseModel):
    id: int
    title: str
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    link_to_description: Optional[str] = None

    class Config:
        orm_mode = True

class JobOffer(JobOfferBase):
    keywords: Optional[List[str]] = None
    company: Optional[List[str]] = None
    recruiters: Optional[List[str]] = None

    class Config:
        orm_mode = True