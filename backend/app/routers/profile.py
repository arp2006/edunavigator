from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models import UserProfile
from app.schemas.profile import ProfileResponse

router = APIRouter()

@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return profile

# @router.patch("/{user_id}", response_model=ProfileResponse)
# def update_profile(user_id: int, updates: ProfileUpdate, db: Session = Depends(get_db)):
#     """Partially update a student profile."""
#     profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
#     if not profile:
#         raise HTTPException(status_code=404, detail="Profile not found")

#     update_data = updates.model_dump(exclude_unset=True)
#     for field, value in update_data.items():
#         setattr(profile, field, value)

#     db.commit()
#     db.refresh(profile)
#     return profile
