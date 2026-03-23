from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models import UserProfile
from app.schemas.profile import ProfileCreate, ProfileResponse, ProfileUpdate

router = APIRouter()


@router.post("/", response_model=ProfileResponse, status_code=201)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    """Create a new student profile with questionnaire data."""
    # Check if email already exists
    existing = db.query(UserProfile).filter(UserProfile.email == profile.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_profile = UserProfile(**profile.model_dump())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.get("/{user_id}", response_model=ProfileResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    """Retrieve a student profile by ID."""
    profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.patch("/{user_id}", response_model=ProfileResponse)
def update_profile(user_id: int, updates: ProfileUpdate, db: Session = Depends(get_db)):
    """Partially update a student profile."""
    profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile
