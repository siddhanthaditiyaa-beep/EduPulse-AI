from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TopicMasteryItem(BaseModel):
    topic_id: int
    topic_name: str
    subject_name: str
    mastery_score: float
    mastery_level: str  # Beginner, Needs Improvement, Developing, Proficient, Mastered
    accuracy: float
    attempts: int
    needs_attention: bool

class AccuracyTrendPoint(BaseModel):
    date: str
    accuracy: float
    topic_name: str

class StudyTimePoint(BaseModel):
    date: str
    minutes: int

class RecentMistakeItem(BaseModel):
    question_id: int
    topic_name: str
    question: str
    your_answer: str
    correct_answer: str
    explanation: str
    date: str

class PerformanceAnalyticsResponse(BaseModel):
    overall_mastery: float
    quiz_average: float
    total_quizzes_taken: int
    total_study_minutes: int
    topics_mastery: List[TopicMasteryItem]
    accuracy_trend: List[AccuracyTrendPoint]
    study_time_trend: List[StudyTimePoint]
    strong_topics: List[str]
    weak_topics: List[str]
    recent_mistakes: List[RecentMistakeItem]
    predicted_score: Optional[float] = None
    prediction_range: Optional[str] = None
    timeframe: str  # 7d, 30d, all
