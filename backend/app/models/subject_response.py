from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.db import Base

class SubjectResponse(Base):
    __tablename__ = "subject_responses"

    id = Column(Integer, primary_key=True)

    profile_id = Column(Integer, ForeignKey("profiles.id"))
    subject = Column(String)  # math, physics, accounts, etc.

    interest = Column(Integer)     # 1–5
    performance = Column(Integer)  # 1–5 (normalized)

    profile = relationship("Profile", back_populates="subject_responses")

    __table_args__ = (
        UniqueConstraint('profile_id', 'subject', name='unique_profile_subject'),
    )