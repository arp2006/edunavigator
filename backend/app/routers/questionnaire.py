from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.questionnaire import QuestionnaireRequest
from app.services.questionnaire_service import process_questionnaire
from app.core.deps import get_current_user

router = APIRouter()


@router.post("/")
def submit_questionnaire(
    data: QuestionnaireRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    user_id = user.get("user_id")

    result = process_questionnaire(user_id, data, db)

    if not result:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {
        "message": "Questionnaire processed successfully"
    }