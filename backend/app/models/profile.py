from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.sql import func
from app.core.db import Base


class UserProfile(Base):
    """Stores student profile and questionnaire responses."""
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    # Aptitude scores (0.0 - 1.0)
    math_score = Column(Float, default=0.5)
    science_score = Column(Float, default=0.5)
    arts_score = Column(Float, default=0.5)
    commerce_score = Column(Float, default=0.5)
    tech_score = Column(Float, default=0.5)

    # Interests and preferences (stored as JSON lists)
    interests = Column(JSON, default=list) 
    preferred_fields = Column(JSON, default=list) 
    work_style = Column(String, default="mixed")  
    career_goal = Column(String, default="")

    # Chat history for the interactive advisor
    chat_history = Column(JSON, default=list)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class DegreeProgram(Base):
    """Static table of available bachelor's degree programs."""
    __tablename__ = "degree_programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    field = Column(String, nullable=False) 
    description = Column(String)

    requires_math = Column(Float, default=0.5)
    requires_science = Column(Float, default=0.5)
    requires_arts = Column(Float, default=0.5)
    requires_commerce = Column(Float, default=0.5)
    requires_tech = Column(Float, default=0.5)

    tags = Column(JSON, default=list) 