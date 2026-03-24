from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.schemas.auth import SignupRequest, LoginRequest
from app.services.auth_service import signup, login

router = APIRouter()

@router.post("/signup")
def signup_user(data: SignupRequest, db: Session = Depends(get_db)):
    user = signup(data, db)

    if not user:
        return {"error": "User already exists"}

    return {"message": "User created", "user_id": user.id}


@router.post("/login")
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    token = login(data, db)

    if not token:
        return {"error": "Invalid credentials"}

    return {
        "access_token": token,
        "token_type": "bearer"
    }