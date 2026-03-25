from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.auth import SignupRequest, LoginRequest
from app.services.auth_service import signup, login

router = APIRouter()

@router.post("/signup")
def signup_user(data: SignupRequest, db: Session = Depends(get_db)):
    user_profile = signup(data, db)

    if not user_profile:
        raise HTTPException(status_code=400, detail="User already exists")

    user, profile = user_profile

    return {
        "message": "User created",
        "user_id": user.id,
        "profile_id": profile.id
    }

@router.post("/login")
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    token = login(data, db)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": token,
        "token_type": "bearer"
    }