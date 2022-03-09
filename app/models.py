from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float, Text
from sqlalchemy.orm import relationship

from .database import Base


class Refugee(Base):
    __tablename__ = "refugee"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    family_name = Column(String(50))
    birth_date = Column(Date)
    salary_targeted = Column(Integer)
    email = Column(String(50))
    # keywords = relationship("Item", back_populates="owner")
    keywords = Column(Text) # text of words separated by a comma (to be ordered and cleaned in the front-end part, before storing in json?)

class EquivalentKeyword(Base):
    __tablename__ = "equikeyword"

    label = Column(String(50), primary_key=True, index=True)
    keyword = Column(String(50), ForeignKey('keyword.label')) # pb how to filter

class Keyword(Base):
    __tablename__ = "keyword"

    label = Column(String(50), primary_key=True, index=True)
