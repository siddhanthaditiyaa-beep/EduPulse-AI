from pydantic import BaseModel, Field
from typing import List, Optional

class AITutorMessage(BaseModel):
    role: str  # user, assistant, system
    content: str

class AITutorRequest(BaseModel):
    message: str
    topic_id: Optional[int] = None
    subject_id: Optional[int] = None
    action_type: Optional[str] = "general"  # explain_simply, give_example, real_world_example, test_me, explain_mistake, general
    context_question_id: Optional[int] = None
    chat_history: Optional[List[AITutorMessage]] = []

class AITutorResponse(BaseModel):
    reply: str
    action_type: str
    topic_name: Optional[str] = None
    student_mastery_level: Optional[str] = None
    follow_up_suggestions: List[str] = []

class AIQuizQuestionGenerated(BaseModel):
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str  # A, B, C, D
    explanation: str
    difficulty: str  # easy, medium, hard

class AIQuizGenerationResponse(BaseModel):
    topic_id: int
    topic_name: str
    difficulty: str
    questions: List[AIQuizQuestionGenerated]
    is_ai_generated: bool = True
