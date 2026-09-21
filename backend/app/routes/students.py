import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.models.profile import StudentProfile
from backend.app.models.performance import TopicPerformance, Prediction
from backend.app.models.assessments import QuizAttempt
from backend.app.models.academic import Topic
from backend.app.models.study import StudyPlan
from backend.app.schemas.student import StudentProfileCreateOrUpdate, StudentProfileDetailResponse, DashboardSummaryResponse
from backend.app.auth.dependencies import get_current_user
from backend.app.services.study_plan_service import generate_daily_study_plan
from backend.app.services.recommendation_service import generate_personalized_recommendations

router = APIRouter(prefix="/students", tags=["Student Management"])

@router.get("/profile", response_model=StudentProfileDetailResponse)
def get_student_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetch student profile settings."""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.put("/profile", response_model=StudentProfileDetailResponse)
def update_student_profile(
    data: StudentProfileCreateOrUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update student onboarding preferences and daily goals."""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)

    profile.education_level = data.education_level or profile.education_level
    profile.learning_goal = data.learning_goal or profile.learning_goal
    profile.preferred_difficulty = data.preferred_difficulty or profile.preferred_difficulty
    profile.daily_study_target = data.daily_study_target or profile.daily_study_target
    profile.updated_at = datetime.datetime.utcnow()

    db.commit()
    db.refresh(profile)
    return profile

@router.get("/dashboard", response_model=DashboardSummaryResponse)
def get_dashboard_summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Returns the comprehensive student dashboard view:
    - Welcome student name (never hard-coded)
    - KPI cards: overall mastery, quiz average, study streak, XP
    - Strong topics & Weak topics
    - Today's personalized learning plan
    - Recent activities
    """
    profile = current_user.profile or db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    
    # Topic performances
    perfs = db.query(TopicPerformance).filter(TopicPerformance.user_id == current_user.id).all()
    overall_mastery = round(sum(p.mastery_score for p in perfs) / len(perfs), 1) if perfs else 0.0

    # Quiz attempts
    quizzes = db.query(QuizAttempt).filter(QuizAttempt.user_id == current_user.id).all()
    quiz_average = round(sum(q.accuracy for q in quizzes) / len(quizzes), 1) if quizzes else 0.0

    # Strong & weak topics
    topics_map = {t.id: t.name for t in db.query(Topic).all()}
    strong_topics = []
    weak_topics = []

    for p in sorted(perfs, key=lambda x: x.mastery_score, reverse=True):
        t_name = topics_map.get(p.topic_id, "Unknown Topic")
        entry = {
            "topic_id": p.topic_id,
            "topic_name": t_name,
            "mastery_score": p.mastery_score,
            "accuracy": p.accuracy,
            "attempts": p.attempts
        }
        if p.mastery_score >= 70.0:
            strong_topics.append(entry)
        elif p.mastery_score < 60.0 or p.attempts > 0 and p.accuracy < 60.0:
            weak_topics.append(entry)

    # Latest ML prediction
    prediction = db.query(Prediction).filter(Prediction.user_id == current_user.id).order_by(Prediction.created_at.desc()).first()
    predicted_score = prediction.predicted_score if prediction else None
    prediction_range = prediction.prediction_range if prediction else None

    # Today's study plan
    study_plan = generate_daily_study_plan(current_user.id, db)
    plan_dict = None
    if study_plan:
        items_list = []
        for it in study_plan.items:
            items_list.append({
                "id": it.id,
                "topic_id": it.topic_id,
                "topic_name": topics_map.get(it.topic_id, ""),
                "activity_type": it.activity_type,
                "duration_minutes": it.duration_minutes,
                "priority": it.priority,
                "completed": it.completed
            })
        plan_dict = {
            "id": study_plan.id,
            "title": study_plan.title,
            "duration": study_plan.duration,
            "items": items_list
        }

    # Recent activity
    recent_activity = []
    recent_quizzes = db.query(QuizAttempt).filter(QuizAttempt.user_id == current_user.id).order_by(QuizAttempt.completed_at.desc()).limit(5).all()
    for q in recent_quizzes:
        recent_activity.append({
            "type": "quiz",
            "topic_name": topics_map.get(q.topic_id, "Quiz"),
            "score": f"{q.score}/{q.total_questions}",
            "accuracy": f"{q.accuracy:.0f}%",
            "date": q.completed_at.strftime("%b %d, %H:%M")
        })

    return {
        "student_name": current_user.name,
        "overall_mastery": overall_mastery,
        "quiz_average": quiz_average,
        "study_streak": profile.streak_days if profile else 1,
        "xp_points": profile.xp_points if profile else 50,
        "predicted_score": predicted_score,
        "prediction_range": prediction_range,
        "strong_topics": strong_topics[:4],
        "weak_topics": weak_topics[:4],
        "today_plan": plan_dict,
        "recent_activity": recent_activity
    }
