from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.models.academic import Topic, Question
from backend.app.models.performance import TopicPerformance
from backend.app.models.assessments import QuestionAttempt
from backend.app.schemas.ai import AITutorRequest, AITutorResponse
from backend.app.auth.dependencies import get_current_user
from backend.app.services.ai_service import ai_service
from backend.app.services.mastery_service import get_mastery_level_label

router = APIRouter(prefix="/ai", tags=["AI Tutoring & Intelligence"])

@router.post("/tutor", response_model=AITutorResponse)
def ask_ai_tutor(
    data: AITutorRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Interacts with the adaptive AI tutor:
    - Automatically looks up student's actual mastery level on the subject/topic
    - Adapts pedagogical complexity (Beginner vs Proficient)
    - Supports action buttons (Explain Simply, Give Example, Real-World Example, Test Me, Explain My Mistake)
    - References specific past mistakes if context_question_id is provided
    """
    topic_name = None
    mastery_score = None
    mastery_level = None

    if data.topic_id:
        topic = db.query(Topic).filter(Topic.id == data.topic_id).first()
        if topic:
            topic_name = topic.name
            perf = db.query(TopicPerformance).filter(
                TopicPerformance.user_id == current_user.id,
                TopicPerformance.topic_id == topic.id
            ).first()
            if perf:
                mastery_score = perf.mastery_score
                mastery_level = get_mastery_level_label(mastery_score)
            else:
                mastery_score = 0.0
                mastery_level = "Beginner"

    context_mistake = None
    if data.context_question_id:
        q = db.query(Question).filter(Question.id == data.context_question_id).first()
        if q:
            # Find student's wrong attempt
            wrong_att = (
                db.query(QuestionAttempt)
                .filter(QuestionAttempt.question_id == q.id, QuestionAttempt.is_correct == False)
                .order_by(QuestionAttempt.id.desc())
                .first()
            )
            context_mistake = {
                "question": q.question,
                "selected_answer": f"Option {wrong_att.selected_answer}" if wrong_att else "Unknown",
                "correct_answer": f"Option {q.correct_answer}",
                "explanation": q.explanation
            }

    # Convert chat history to dict format
    history_dicts = [{"role": m.role, "content": m.content} for m in data.chat_history] if data.chat_history else []

    result = ai_service.generate_ai_tutor_response(
        student_message=data.message,
        student_name=current_user.name,
        action_type=data.action_type or "general",
        topic_name=topic_name,
        mastery_score=mastery_score,
        mastery_level=mastery_level,
        chat_history=history_dicts,
        context_mistake=context_mistake
    )

    return result
