import datetime
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class TopicPerformance(Base):
    __tablename__ = "topic_performance"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    accuracy = Column(Float, default=0.0)  # Average accuracy percentage
    mastery_score = Column(Float, default=0.0)  # Calculated 0.0 to 100.0
    attempts = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="topic_performances")
    topic = relationship("Topic", back_populates="topic_performances")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    predicted_score = Column(Float, nullable=False)  # Estimate 0 - 100
    prediction_range = Column(String(50), nullable=False)  # e.g. "72.4 - 84.1"
    model_name = Column(String(100), default="RandomForestRegressor")
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="predictions")
