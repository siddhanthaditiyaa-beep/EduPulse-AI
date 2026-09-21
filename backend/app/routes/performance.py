import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.models.academic import Topic, Question, Subject
from backend.app.models.performance import TopicPerformance, Prediction
from backend.app.models.assessments import QuizAttempt, QuestionAttempt
from backend.app.models.study import StudySession
from backend.app.models.recommendations import Recommendation
from backend.app.schemas.analytics import PerformanceAnalyticsResponse
from backend.app.auth.dependencies import get_current_user
from backend.app.services.mastery_service import get_mastery_level_label
from backend.app.services.ml_prediction_service import ml_service
from backend.app.services.recommendation_service import generate_personalized_recommendations

router = APIRouter(prefix="/performance", tags=["Performance Analytics & Predictions"])

@router.get("", response_model=PerformanceAnalyticsResponse)
def get_performance_analytics(
    timeframe: str = Query("30d", regex="^(7d|30d|all)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns deep performance analytics:
    - Timeframe filtering (7d, 30d, all)
    - Overall mastery & average quiz accuracy
    - Topic-by-topic mastery breakdown for the Knowledge Map
    - Accuracy trend over time
    - Study time trend
    - Strong & weak topics
    - Recent mistakes with explanations
    - Latest ML performance prediction
    """
    now = datetime.datetime.utcnow()
    cutoff_date = None
    if timeframe == "7d":
        cutoff_date = now - datetime.timedelta(days=7)
    elif timeframe == "30d":
        cutoff_date = now - datetime.timedelta(days=30)

    # Filter quizzes by timeframe
    quiz_query = db.query(QuizAttempt).filter(QuizAttempt.user_id == current_user.id)
    if cutoff_date:
        quiz_query = quiz_query.filter(QuizAttempt.completed_at >= cutoff_date)
    quizzes = quiz_query.order_by(QuizAttempt.completed_at.asc()).all()

    # Filter sessions by timeframe
    sess_query = db.query(StudySession).filter(StudySession.user_id == current_user.id)
    if cutoff_date:
        sess_query = sess_query.filter(StudySession.completed_at >= cutoff_date)
    sessions = sess_query.all()

    total_study_minutes = sum(s.duration_minutes for s in sessions)
    quiz_average = round(sum(q.accuracy for q in quizzes) / len(quizzes), 1) if quizzes else 0.0

    # Topic performance
    topics = db.query(Topic).order_by(Topic.order_index.asc()).all()
    topics_map = {t.id: t for t in topics}
    perfs = db.query(TopicPerformance).filter(TopicPerformance.user_id == current_user.id).all()
    perf_dict = {p.topic_id: p for p in perfs}

    topics_mastery_list = []
    strong_topics = []
    weak_topics = []

    for t in topics:
        p = perf_dict.get(t.id)
        m_score = p.mastery_score if p else 0.0
        acc = p.accuracy if p else 0.0
        att = p.attempts if p else 0
        lvl = get_mastery_level_label(m_score)
        needs_attention = (m_score < 60.0)

        topics_mastery_list.append({
            "topic_id": t.id,
            "topic_name": t.name,
            "subject_name": t.subject.name if t.subject else "DBMS",
            "mastery_score": m_score,
            "mastery_level": lvl,
            "accuracy": acc,
            "attempts": att,
            "needs_attention": needs_attention
        })

        if m_score >= 75.0:
            strong_topics.append(t.name)
        elif m_score < 60.0 and (att > 0 or p is not None):
            weak_topics.append(t.name)

    overall_mastery = round(sum(item["mastery_score"] for item in topics_mastery_list) / len(topics_mastery_list), 1) if topics_mastery_list else 0.0

    # Accuracy trend
    accuracy_trend = []
    for q in quizzes:
        t = topics_map.get(q.topic_id)
        accuracy_trend.append({
            "date": q.completed_at.strftime("%b %d"),
            "accuracy": q.accuracy,
            "topic_name": t.name if t else "Quiz"
        })

    # Study time trend aggregated by date
    daily_study = {}
    for s in sessions:
        d_str = s.completed_at.strftime("%b %d")
        daily_study[d_str] = daily_study.get(d_str, 0) + s.duration_minutes
    study_time_trend = [{"date": k, "minutes": v} for k, v in daily_study.items()]

    # Recent mistakes
    recent_mistakes = []
    mistake_attempts = (
        db.query(QuestionAttempt)
        .join(QuizAttempt)
        .filter(QuizAttempt.user_id == current_user.id, QuestionAttempt.is_correct == False)
        .order_by(QuizAttempt.completed_at.desc())
        .limit(5)
        .all()
    )
    for ma in mistake_attempts:
        q = ma.question
        t = topics_map.get(q.topic_id) if q else None
        if q:
            recent_mistakes.append({
                "question_id": q.id,
                "topic_name": t.name if t else "DBMS",
                "question": q.question,
                "your_answer": f"Option {ma.selected_answer}",
                "correct_answer": f"Option {q.correct_answer}",
                "explanation": q.explanation,
                "date": ma.quiz_attempt.completed_at.strftime("%b %d")
            })

    # Latest ML prediction
    prediction = db.query(Prediction).filter(Prediction.user_id == current_user.id).order_by(Prediction.created_at.desc()).first()
    predicted_score = prediction.predicted_score if prediction else None
    prediction_range = prediction.prediction_range if prediction else None

    return {
        "overall_mastery": overall_mastery,
        "quiz_average": quiz_average,
        "total_quizzes_taken": len(quizzes),
        "total_study_minutes": total_study_minutes,
        "topics_mastery": topics_mastery_list,
        "accuracy_trend": accuracy_trend,
        "study_time_trend": study_time_trend,
        "strong_topics": strong_topics,
        "weak_topics": weak_topics,
        "recent_mistakes": recent_mistakes,
        "predicted_score": predicted_score,
        "prediction_range": prediction_range,
        "timeframe": timeframe
    }

@router.get("/prediction")
def get_or_calculate_prediction(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Calculates or retrieves the latest ML performance prediction."""
    return ml_service.predict_performance(current_user.id, db)

@router.get("/recommendations")
def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Fetches personalized study recommendations based on real performance data."""
    recs = db.query(Recommendation).filter(
        Recommendation.user_id == current_user.id,
        Recommendation.completed == False
    ).order_by(Recommendation.created_at.desc()).limit(6).all()

    if not recs:
        recs = generate_personalized_recommendations(current_user.id, db)

    topics_map = {t.id: t.name for t in db.query(Topic).all()}

    return [
        {
            "id": r.id,
            "topic_id": r.topic_id,
            "topic_name": topics_map.get(r.topic_id, "Topic"),
            "recommendation_type": r.recommendation_type,
            "priority": r.priority,
            "reason": r.reason,
            "completed": r.completed,
            "created_at": r.created_at
        }
        for r in recs
    ]
