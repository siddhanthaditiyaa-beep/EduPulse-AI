from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class StudentProfileCreateOrUpdate(BaseModel):
    education_level: Optional[str] = "Undergraduate"
    learning_goal: Optional[str] = "Semester Exam Preparation"
    preferred_difficulty: Optional[str] = "medium"
    daily_study_target: Optional[int] = Field(default=45, ge=10, le=480)
    selected_subjects: Optional[List[str]] = None

class StudentProfileDetailResponse(BaseModel):
    id: int
    user_id: int
    education_level: str
    learning_goal: str
    preferred_difficulty: str
    daily_study_target: int
    xp_points: int
    streak_days: int
    last_active_date: Optional[str] = None
    badges_json: Optional[str] = "[]"
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DashboardSummaryResponse(BaseModel):
    student_name: str
    overall_mastery: float
    quiz_average: float
    study_streak: int
    xp_points: int
    predicted_score: Optional[float] = None
    prediction_range: Optional[str] = None
    strong_topics: List[dict] = []
    weak_topics: List[dict] = []
    today_plan: Optional[dict] = None
    recent_activity: List[dict] = []
