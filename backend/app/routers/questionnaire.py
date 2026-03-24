from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.questionnaire import QuestionnaireSubmission
from app.services.questionnaire_service import process_and_store_answers

router = APIRouter()

@router.post("/")
def submit_questionnaire(data: QuestionnaireSubmission, db: Session = Depends(get_db)):
    result = process_and_store_answers(data, db)

    if not result:
        return {"error": "User not found"}

    user, recommendations = result

    return {
        "message": "Questionnaire processed",
        "user_id": user.id,
        "recommendations": recommendations
    }