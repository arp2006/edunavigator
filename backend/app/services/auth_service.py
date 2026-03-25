from app.models.user import User
from app.core.security import hash_password
from app.core.security import verify_password
from app.core.jwt_handler import create_access_token
from app.models.profile import UserProfile

def signup(data, db):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        return None

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password)
    )

    db.add(user)
    db.flush()  # get user.id without commit

    profile = UserProfile(
        user_id=user.id,
        stream=data.stream
    )

    db.add(profile)
    db.commit()

    db.refresh(user)
    db.refresh(profile)

    return user, profile

def login(data, db):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        return None

    if not verify_password(data.password, user.hashed_password):
        return None

    token = create_access_token({"user_id": user.id})

    return token