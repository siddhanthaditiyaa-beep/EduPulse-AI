from backend.app.schemas.auth import UserRegister, UserLogin, Token, UserResponse, StudentProfileDTO
from backend.app.schemas.student import StudentProfileCreateOrUpdate, StudentProfileDetailResponse, DashboardSummaryResponse
from backend.app.schemas.academic import SubjectResponse, TopicSummaryResponse, TopicDetailResponse, LearningMaterialResponse, QuestionResponse
from backend.app.schemas.quiz import QuizGenerateRequest, QuizSubmitRequest, QuizResultResponse, DiagnosticSubmitRequest, DiagnosticResultResponse
from backend.app.schemas.analytics import PerformanceAnalyticsResponse, TopicMasteryItem
from backend.app.schemas.ai import AITutorRequest, AITutorResponse, AIQuizGenerationResponse

__all__ = [
    "UserRegister",
    "UserLogin",
    "Token",
    "UserResponse",
    "StudentProfileDTO",
    "StudentProfileCreateOrUpdate",
    "StudentProfileDetailResponse",
    "DashboardSummaryResponse",
    "SubjectResponse",
    "TopicSummaryResponse",
    "TopicDetailResponse",
    "LearningMaterialResponse",
    "QuestionResponse",
    "QuizGenerateRequest",
    "QuizSubmitRequest",
    "QuizResultResponse",
    "DiagnosticSubmitRequest",
    "DiagnosticResultResponse",
    "PerformanceAnalyticsResponse",
    "TopicMasteryItem",
    "AITutorRequest",
    "AITutorResponse",
    "AIQuizGenerationResponse",
]
