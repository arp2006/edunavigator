from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models import UserProfile
from app.schemas.chat import ChatMessage, ChatResponse
from app.services.recommendation_service import generate_recommendations
from app.services.chat_service import parse_chat_input

router = APIRouter()


# ─── Simple Intent Parser ─────────────────────────────────────────────────────

# ─── Route ────────────────────────────────────────────────────────────────────

@router.post("/", response_model=ChatResponse)
def chat(message: ChatMessage, db: Session = Depends(get_db)):
    """
    Accept a natural language message from the user, update their profile
    based on detected intent, and return refreshed recommendations.
    """
    profile = db.query(UserProfile).filter(UserProfile.id == message.user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Parse chat input for profile update signals
    parsed = parse_chat_input(message.message)

    # Append message to chat history
    chat_history = list(profile.chat_history or [])
    chat_history.append({"role": "user", "message": message.message})

    # Apply updates to profile
    updates = parsed["updates"]
    for field, value in updates.items():
        setattr(profile, field, value)
    profile.chat_history = chat_history

    db.commit()
    db.refresh(profile)

    # Recompute recommendations with updated profile
    updated_recommendations = generate_recommendations(profile, top_n=5)

    return ChatResponse(
        reply=parsed["reply"],
        updated_recommendations=updated_recommendations
    )
