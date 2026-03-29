from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.db import Base


class DegreeType(Base):
    __tablename__ = "degree_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    disciplines = relationship("Discipline", back_populates="field")


class Discipline(Base):
    __tablename__ = "disciplines"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    field_id = Column(Integer, ForeignKey("fields.id"))
    field = relationship("Field", back_populates="disciplines")


class Degree(Base):
    __tablename__ = "degrees"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    type_id = Column(Integer, ForeignKey("degree_types.id"), nullable=False)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=False)
    discipline_id = Column(Integer, ForeignKey("disciplines.id"), nullable=False)

    type = relationship("DegreeType")
    field = relationship("Field")
    discipline = relationship("Discipline")

    math_weight = Column(Float, default=0.0)
    tech_weight = Column(Float, default=0.0)
    arts_weight = Column(Float, default=0.0)
    commerce_weight = Column(Float, default=0.0)
    science_weight = Column(Float, default=0.0)