import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class DiagnosticTest(Base):
    __tablename__ = "diagnostic_tests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    score = Column(Float, nullable=False)  # Percentage score 0 - 100
    completed_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="diagnostic_tests")
    subject = relationship("Subject", back_populates="diagnostic_tests")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, nullable=False)  # Number of correct questions
    total_questions = Column(Integer, nullable=False)
    accuracy = Column(Float, nullable=False)  # Score / total_questions * 100
    difficulty = Column(String(50), default="medium")
    completed_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="quiz_attempts")
    topic = relationship("Topic", back_populates="quiz_attempts")
    question_attempts = relationship("QuestionAttempt", back_populates="quiz_attempt", cascade="all, delete-orphan")

class QuestionAttempt(Base):
    __tablename__ = "question_attempts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quiz_attempt_id = Column(Integer, ForeignKey("quiz_attempts.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    selected_answer = Column(String(10), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    response_time = Column(Integer, default=0)  # In seconds

    quiz_attempt = relationship("QuizAttempt", back_populates="question_attempts")
    question = relationship("Question", back_populates="question_attempts")
