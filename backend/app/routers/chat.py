from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.deps import get_current_user
from app.schemas.chat import ChatMessage, ChatResponse
from app.services.chat_service import process_chat
from app.services.recommendation_service import generate_recommendations

router = APIRouter()


@router.post("/", response_model=ChatResponse)
def chat(
    message: ChatMessage,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    user_id = user.get("user_id")

    try:
        result = process_chat(message.profile_id, message.message, db)
    except ValueError as e:
        status = 429 if "rate limit" in str(e).lower() else 502
        raise HTTPException(status_code=status, detail=str(e))

    if result is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile = result["profile"]

    # Recompute recommendations with updated scores
    updated_recommendations = generate_recommendations(profile.id, db, top_n=10)

    return ChatResponse(
        reply=result["reply"],
        updated_recommendations=updated_recommendations
    )


@router.get("/history/{profile_id}")
def get_history(
    profile_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    from app.models import UserProfile
    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"history": profile.chat_history or []}