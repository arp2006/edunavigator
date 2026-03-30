from pydantic import BaseModel
from typing import List, Optional


class DegreeRecommendation(BaseModel):
    degree_name: str
    type: str
    field: str
    discipline: str
    score: float

    # ✅ ADD THESE
    confidence: Optional[float] = None
    why: Optional[str] = None


class RecommendationResponse(BaseModel):
    profile_id: int
    recommendations: List[DegreeRecommendation]