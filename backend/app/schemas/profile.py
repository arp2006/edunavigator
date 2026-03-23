from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


class ProfileCreate(BaseModel):
    name: str
    email: EmailStr
    math_score: float = 0.5
    science_score: float = 0.5
    arts_score: float = 0.5
    commerce_score: float = 0.5
    tech_score: float = 0.5
    interests: List[str] = Field(default_factory=list)
    preferred_fields: List[str] = Field(default_factory=list)
    work_style: str = "mixed"
    career_goal: str = ""


class ProfileUpdate(BaseModel):
    math_score: Optional[float] = None
    science_score: Optional[float] = None
    arts_score: Optional[float] = None
    commerce_score: Optional[float] = None
    tech_score: Optional[float] = None
    interests: Optional[List[str]] = None
    preferred_fields: Optional[List[str]] = None
    work_style: Optional[str] = None
    career_goal: Optional[str] = None


class ProfileResponse(BaseModel):
    id: int
    name: str
    email: str
    math_score: float
    science_score: float
    arts_score: float
    commerce_score: float
    tech_score: float
    interests: List[str]
    preferred_fields: List[str]
    work_style: str
    career_goal: str
    created_at: Optional[datetime]

    class Config:
        from_attributes = True