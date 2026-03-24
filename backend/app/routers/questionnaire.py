from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.questionnaire import QuestionnaireSubmission
from app.services.questionnaire_service import process_and_store_answers
from app.core.deps import get_current_user

router = APIRouter()

@router.post("/")
def submit_questionnaire(
    data: QuestionnaireSubmission,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)   # 👈 from JWT
):
    user_id = user.get("user_id")

    result = process_and_store_answers(user_id, data, db)

    if not result:
        return {"error": "User not found"}

    user_obj, recommendations = result

    return {
        "message": "Questionnaire processed",
        "user_id": user_obj.id,
        "recommendations": recommendations
    }