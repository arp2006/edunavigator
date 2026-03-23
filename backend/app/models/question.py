from sqlalchemy import Column, Integer, String, Float
from app.core.db import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    category = Column(String, nullable=False)   # math, tech, etc.
    weight = Column(Float, default=1.0)