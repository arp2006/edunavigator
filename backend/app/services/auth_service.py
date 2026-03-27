from app.models.user import User
from app.models.profile import UserProfile
from app.core.security import hash_password
from app.core.security import verify_password
from app.core.jwt_handler import create_access_token

def signup(data, db):
    try:
        existing = db.query(User).filter(User.email == data.email).first()
        if existing:
            return None

        user = User(
            name=data.name,
            email=data.email,
            hashed_password=hash_password(data.password)
        )

        db.add(user)
        db.flush()

        profile = UserProfile(
            user_id=user.id,
            stream=data.stream
        )

        db.add(profile)
        db.commit()

        db.refresh(user)
        db.refresh(profile)

        token = create_access_token({"user_id": user.id})

        return token, user, profile

    except Exception as e:
        db.rollback()
        raise e

def login(data, db):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        return None

    if not verify_password(data.password, user.hashed_password):
        return None

    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()

    token = create_access_token({"user_id": user.id})

    return token, user, profile