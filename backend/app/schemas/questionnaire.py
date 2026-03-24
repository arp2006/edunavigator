from pydantic import BaseModel
from typing import List

class AnswerItem(BaseModel):
    question_id: int
    answer: str   # "yes", "no", "maybe"

class QuestionnaireSubmission(BaseModel):
    user_id: int
    answers: List[AnswerItem]