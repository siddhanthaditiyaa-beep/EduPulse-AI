from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.models.academic import Subject, Topic, LearningMaterial
from backend.app.models.performance import TopicPerformance
from backend.app.models.assessments import DiagnosticTest
from backend.app.schemas.academic import SubjectResponse, TopicSummaryResponse, TopicDetailResponse, LearningMaterialResponse
from backend.app.auth.dependencies import get_current_user

router = APIRouter(prefix="/subjects", tags=["Curriculum & Topics"])

@router.get("", response_model=List[SubjectResponse])
def get_all_subjects(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """List all available subjects with topic count and student progress."""
    subjects = db.query(Subject).all()
    results = []
    
    for s in subjects:
        topics_count = len(s.topics)
        diag = db.query(DiagnosticTest).filter(
            DiagnosticTest.user_id == current_user.id,
            DiagnosticTest.subject_id == s.id
        ).first()
        
        # Average mastery in this subject
        topic_ids = [t.id for t in s.topics]
        perfs = db.query(TopicPerformance).filter(
            TopicPerformance.user_id == current_user.id,
            TopicPerformance.topic_id.in_(topic_ids)
        ).all()
        avg_mastery = round(sum(p.mastery_score for p in perfs) / len(perfs), 1) if perfs else 0.0

        results.append({
            "id": s.id,
            "name": s.name,
            "description": s.description,
            "topics_count": topics_count,
            "diagnostic_completed": diag is not None,
            "average_mastery": avg_mastery
        })
    return results

@router.get("/{subject_id}/topics", response_model=List[TopicSummaryResponse])
def get_subject_topics(subject_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetch all topics for a given subject along with current student mastery."""
    topics = db.query(Topic).filter(Topic.subject_id == subject_id).order_by(Topic.order_index.asc()).all()
    if not topics:
        raise HTTPException(status_code=404, detail="Subject not found or has no topics")

    topic_ids = [t.id for t in topics]
    perf_dict = {p.topic_id: p for p in db.query(TopicPerformance).filter(
        TopicPerformance.user_id == current_user.id,
        TopicPerformance.topic_id.in_(topic_ids)
    ).all()}

    summary = []
    for t in topics:
        p = perf_dict.get(t.id)
        summary.append({
            "id": t.id,
            "subject_id": t.subject_id,
            "name": t.name,
            "description": t.description,
            "difficulty": t.difficulty,
            "order_index": t.order_index,
            "mastery_score": p.mastery_score if p else 0.0,
            "accuracy": p.accuracy if p else 0.0,
            "attempts": p.attempts if p else 0
        })
    return summary

@router.get("/topics/{topic_id}", response_model=TopicDetailResponse)
def get_topic_detail(topic_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get rich educational materials, notes, and progress for a topic."""
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    perf = db.query(TopicPerformance).filter(
        TopicPerformance.user_id == current_user.id,
        TopicPerformance.topic_id == topic_id
    ).first()

    return {
        "id": topic.id,
        "subject_id": topic.subject_id,
        "name": topic.name,
        "description": topic.description,
        "difficulty": topic.difficulty,
        "order_index": topic.order_index,
        "materials": topic.learning_materials,
        "mastery_score": perf.mastery_score if perf else 0.0,
        "accuracy": perf.accuracy if perf else 0.0,
        "attempts": perf.attempts if perf else 0
    }
