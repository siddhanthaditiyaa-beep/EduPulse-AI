from pydantic import BaseModel
from typing import Optional, List

class LearningMaterialResponse(BaseModel):
    id: int
    topic_id: int
    title: str
    description: Optional[str] = None
    content: str
    material_type: str
    difficulty: str

    class Config:
        from_attributes = True

class QuestionResponse(BaseModel):
    id: int
    topic_id: int
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty: str
    # Note: correct_answer and explanation are deliberately omitted here for test attempts!

    class Config:
        from_attributes = True

class TopicSummaryResponse(BaseModel):
    id: int
    subject_id: int
    name: str
    description: Optional[str] = None
    difficulty: str
    order_index: int
    mastery_score: Optional[float] = 0.0
    accuracy: Optional[float] = 0.0
    attempts: Optional[int] = 0

    class Config:
        from_attributes = True

class TopicDetailResponse(BaseModel):
    id: int
    subject_id: int
    name: str
    description: Optional[str] = None
    difficulty: str
    order_index: int
    materials: List[LearningMaterialResponse] = []
    mastery_score: float = 0.0
    accuracy: float = 0.0
    attempts: int = 0

    class Config:
        from_attributes = True

class SubjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    topics_count: int = 0
    diagnostic_completed: bool = False
    average_mastery: float = 0.0

    class Config:
        from_attributes = True
