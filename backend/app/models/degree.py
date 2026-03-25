from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.db import Base

class DegreeType(Base):
    __tablename__ = "degree_types"

    id = Column(Integer, primary_key=True)
    name = Column(String)  # bachelors, masters

class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True)
    name = Column(String)  # engineering, science, business

class Discipline(Base):
    __tablename__ = "disciplines"

    id = Column(Integer, primary_key=True)
    name = Column(String)  # CSE, IT, Zoology, Finance

    field_id = Column(Integer, ForeignKey("fields.id"))

class Degree(Base):
    __tablename__ = "degrees"

    id = Column(Integer, primary_key=True)

    name = Column(String)  # B.Tech CSE

    type_id = Column(Integer, ForeignKey("degree_types.id"))
    field_id = Column(Integer, ForeignKey("fields.id"))
    discipline_id = Column(Integer, ForeignKey("disciplines.id"))

    math_weight = Column(Integer)
    tech_weight = Column(Integer)
    arts_weight = Column(Integer)
    commerce_weight = Column(Integer)
    science_weight = Column(Integer)