from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class SubjectInput(BaseModel):
    subject: str
    interest: Optional[int]
    performance: Optional[int]

class QuestionnaireRequest(BaseModel):
    profile_id: int
    responses: List[SubjectInput]
    extra: Optional[Dict[str, Dict[int, int]]] = None

class QuestionnaireResponse(BaseModel):
    message: str