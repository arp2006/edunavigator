from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models import UserProfile
from app.schemas.recommendation import RecommendationResponse
from app.services.recommendation_service import generate_recommendations

router = APIRouter()


@router.get("/{profile_id}", response_model=RecommendationResponse)
def get_recommendations(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    recommendations = generate_recommendations(profile_id, db)

    return RecommendationResponse(
        profile_id=profile_id,
        recommendations=recommendations
    )