from pydantic import BaseModel
from typing import List
from app.schemas.recommendation import DegreeRecommendation

class ChatMessage(BaseModel):
    profile_id: int
    message: str

class ChatResponse(BaseModel):
    reply: str
    updated_recommendations: List[DegreeRecommendation]
