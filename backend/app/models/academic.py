import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")
    diagnostic_tests = relationship("DiagnosticTest", back_populates="subject", cascade="all, delete-orphan")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    difficulty = Column(String(50), default="medium")  # easy, medium, hard
    order_index = Column(Integer, default=0)

    subject = relationship("Subject", back_populates="topics")
    learning_materials = relationship("LearningMaterial", back_populates="topic", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="topic", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="topic", cascade="all, delete-orphan")
    topic_performances = relationship("TopicPerformance", back_populates="topic", cascade="all, delete-orphan")
    study_sessions = relationship("StudySession", back_populates="topic", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="topic", cascade="all, delete-orphan")
    study_plan_items = relationship("StudyPlanItem", back_populates="topic", cascade="all, delete-orphan")

class LearningMaterial(Base):
    __tablename__ = "learning_materials"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=False)  # Markdown or rich HTML content
    material_type = Column(String(50), default="concept_notes")  # concept_notes, summary, examples, cheatsheet
    difficulty = Column(String(50), default="medium")

    topic = relationship("Topic", back_populates="learning_materials")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    question = Column(Text, nullable=False)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    correct_answer = Column(String(10), nullable=False)  # A, B, C, D
    explanation = Column(Text, nullable=False)
    difficulty = Column(String(50), default="medium")  # easy, medium, hard

    topic = relationship("Topic", back_populates="questions")
    question_attempts = relationship("QuestionAttempt", back_populates="question", cascade="all, delete-orphan")
