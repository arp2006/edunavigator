from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base

class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True)

    profile_id = Column(Integer, ForeignKey("profiles.id"), unique=True)

    math_score = Column(Integer, default=0)
    tech_score = Column(Integer, default=0)
    arts_score = Column(Integer, default=0)
    commerce_score = Column(Integer, default=0)
    science_score = Column(Integer, default=0)
    
    score = relationship("Score", back_populates="profile", uselist=False)