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
