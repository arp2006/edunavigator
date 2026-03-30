from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base

class UserProfile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    stream = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    chat_history = Column(JSON, default=list)

    user = relationship("User", backref="profiles")
    subject_responses = relationship("SubjectResponse", back_populates="profile")
    score = relationship("Score", back_populates="profile", uselist=False)