import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    education_level = Column(String(100), default="Undergraduate")
    learning_goal = Column(String(255), default="Semester Exam Preparation")
    preferred_difficulty = Column(String(50), default="medium")
    daily_study_target = Column(Integer, default=45)  # in minutes
    
    # Gamification extensions
    xp_points = Column(Integer, default=0)
    streak_days = Column(Integer, default=1)
    last_active_date = Column(String(20), nullable=True)
    badges_json = Column(Text, default="[]")

    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="profile")
