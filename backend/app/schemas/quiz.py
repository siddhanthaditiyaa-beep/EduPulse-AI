from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class QuizGenerateRequest(BaseModel):
    subject_id: Optional[int] = None
    topic_id: int
    number_of_questions: int = Field(default=5, ge=1, le=20)
    difficulty: Optional[str] = "medium"  # easy, medium, hard, mixed

class QuizAnswerItem(BaseModel):
    question_id: int
    selected_answer: str  # A, B, C, D
    response_time: int = 0  # In seconds

class QuizSubmitRequest(BaseModel):
    topic_id: int
    difficulty: str = "medium"
    answers: List[QuizAnswerItem]

class QuestionResultDetail(BaseModel):
    question_id: int
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    selected_answer: str
    correct_answer: str
    is_correct: bool
    explanation: str
    response_time: int

class QuizResultResponse(BaseModel):
    attempt_id: int
    topic_id: int
    topic_name: str
    score: int
    total_questions: int
    accuracy: float
    difficulty: str
    xp_earned: int
    old_mastery: float
    new_mastery: float
    mistakes_count: int
    details: List[QuestionResultDetail]
    completed_at: datetime

class DiagnosticSubmitItem(BaseModel):
    question_id: int
    selected_answer: str
    topic_id: int

class DiagnosticSubmitRequest(BaseModel):
    subject_id: int
    answers: List[DiagnosticSubmitItem]

class DiagnosticResultResponse(BaseModel):
    test_id: int
    subject_id: int
    subject_name: str
    overall_score: float
    total_questions: int
    correct_answers: int
    topic_breakdown: List[dict]
    strong_topics: List[str]
    weak_topics: List[str]
    initial_plan_generated: bool
    completed_at: datetime
