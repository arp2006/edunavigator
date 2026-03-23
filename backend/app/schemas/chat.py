from pydantic import BaseModel
from typing import List
from app.schemas.recommendation import DegreeRecommendation

class ChatMessage(BaseModel):
    user_id: int
    message: str          # User's natural language input

class ChatResponse(BaseModel):
    reply: str
    updated_recommendations: List[DegreeRecommendation]
