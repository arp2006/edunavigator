from pydantic import BaseModel
from typing import List

class DegreeRecommendation(BaseModel):
    degree_name: str
    field: str
    description: str
    score: float          # 0.0 - 1.0 match score
    match_reason: str     # Human-readable explanation


class RecommendationResponse(BaseModel):
    user_id: int
    recommendations: List[DegreeRecommendation]