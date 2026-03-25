from pydantic import BaseModel, Field
from typing import List

class SubjectInput(BaseModel):
    subject: str
    interest: int = Field(ge=1, le=5)
    performance: int = Field(ge=1, le=5)

class QuestionnaireRequest(BaseModel):
    profile_id: int
    responses: List[SubjectInput]

class QuestionnaireResponse(BaseModel):
    message: str