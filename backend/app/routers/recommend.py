from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models import UserProfile
from app.schemas.recommendation import RecommendationResponse
from app.services.recommendation_service import generate_recommendations

router = APIRouter()


@router.get("/{user_id}", response_model=RecommendationResponse)
def get_recommendations(user_id: int, top_n: int = 5, db: Session = Depends(get_db)):
    """
    Generate personalized degree recommendations for a student.
    Returns top_n ranked degrees (default 5).
    """
    profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    recommendations = generate_recommendations(profile, top_n=top_n)

    return RecommendationResponse(
        user_id=user_id,
        recommendations=recommendations
    )
