from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.db import Base

class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    answer = Column(String, nullable=False)  # "yes", "no", "maybe", etc.

    created_at = Column(DateTime(timezone=True), server_default=func.now())