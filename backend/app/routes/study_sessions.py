import datetime
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.models.academic import Topic
from backend.app.models.study import StudySession
from backend.app.auth.dependencies import get_current_user

router = APIRouter(prefix="/study-session", tags=["Study Sessions"])

class StudySessionLogRequest(BaseModel):
    topic_id: int
    duration_minutes: int = Field(..., ge=1, le=600)
    completed_topic: bool = False

@router.post("/log")
def log_study_session(
    data: StudySessionLogRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log a completed active study session."""
    topic = db.query(Topic).filter(Topic.id == data.topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    session = StudySession(
        user_id=current_user.id,
        topic_id=data.topic_id,
        duration_minutes=data.duration_minutes,
        completed_topic=data.completed_topic,
        completed_at=datetime.datetime.utcnow()
    )
    db.add(session)

    # Award XP: 1 XP per minute studied + 25 bonus if completed
    xp_bonus = data.duration_minutes + (25 if data.completed_topic else 0)
    if current_user.profile:
        current_user.profile.xp_points += xp_bonus

    db.commit()
    db.refresh(session)

    return {
        "session_id": session.id,
        "topic_name": topic.name,
        "duration_minutes": session.duration_minutes,
        "completed_topic": session.completed_topic,
        "xp_earned": xp_bonus,
        "message": f"Great job! You studied {topic.name} for {data.duration_minutes} minutes."
    }

@router.get("/history")
def get_study_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve student study sessions history."""
    sessions = db.query(StudySession).filter(
        StudySession.user_id == current_user.id
    ).order_by(StudySession.completed_at.desc()).limit(20).all()

    topics_map = {t.id: t.name for t in db.query(Topic).all()}

    return [
        {
            "id": s.id,
            "topic_id": s.topic_id,
            "topic_name": topics_map.get(s.topic_id, "Topic"),
            "duration_minutes": s.duration_minutes,
            "completed_topic": s.completed_topic,
            "completed_at": s.completed_at
        }
        for s in sessions
    ]
