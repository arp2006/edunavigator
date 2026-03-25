from pydantic import BaseModel
from typing import List

class DegreeRecommendation(BaseModel):
    degree_name: str
    type: str
    field: str
    discipline: str
    score: float

class RecommendationResponse(BaseModel):
    profile_id: int
    recommendations: List[DegreeRecommendation]