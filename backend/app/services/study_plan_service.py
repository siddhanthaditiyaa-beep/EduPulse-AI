from sqlalchemy.orm import Session
from backend.app.models.profile import StudentProfile
from backend.app.models.academic import Topic
from backend.app.models.performance import TopicPerformance
from backend.app.models.study import StudyPlan, StudyPlanItem
import datetime

def generate_daily_study_plan(user_id: int, db: Session) -> StudyPlan:
    """
    Generates a personalized daily study plan strictly respecting the student's available daily study time.
    Distributes time between:
    1. Weakest topic revision (40% time)
    2. Interactive practice / Quiz (30% time)
    3. New topic or concept deep-dive (30% time)
    """
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()
    target_minutes = profile.daily_study_target if profile and profile.daily_study_target else 45

    # Check for existing plan created today
    today_start = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    existing_plan = db.query(StudyPlan).filter(
        StudyPlan.user_id == user_id,
        StudyPlan.created_at >= today_start
    ).order_by(StudyPlan.created_at.desc()).first()

    if existing_plan and len(existing_plan.items) > 0:
        return existing_plan

    # Fetch topics and performances
    topics = db.query(Topic).order_by(Topic.order_index.asc()).all()
    performances = {p.topic_id: p for p in db.query(TopicPerformance).filter(TopicPerformance.user_id == user_id).all()}

    # Identify weakest topic
    weak_candidates = [
        (t, performances[t.id].mastery_score)
        for t in topics if t.id in performances and performances[t.id].mastery_score < 70
    ]
    weak_candidates.sort(key=lambda x: x[1])

    weak_topic = weak_candidates[0][0] if weak_candidates else (topics[0] if topics else None)

    # Identify unstarted or developing topic
    unstarted = [t for t in topics if t.id not in performances or performances[t.id].attempts == 0]
    next_topic = unstarted[0] if unstarted else (topics[1] if len(topics) > 1 else weak_topic)

    # Time budget allocation
    time_weak = max(10, int(target_minutes * 0.40))
    time_quiz = max(10, int(target_minutes * 0.30))
    time_next = max(10, target_minutes - time_weak - time_quiz)

    plan = StudyPlan(
        user_id=user_id,
        title=f"Personalized Plan for {datetime.datetime.utcnow().strftime('%A, %B %d')}",
        description=f"Tailored study schedule designed for your {target_minutes}-minute daily target.",
        duration=target_minutes,
        created_at=datetime.datetime.utcnow()
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)

    items = []
    if weak_topic:
        items.append(StudyPlanItem(
            study_plan_id=plan.id,
            topic_id=weak_topic.id,
            activity_type="Review Core Concepts & Notes",
            duration_minutes=time_weak,
            priority="high",
            completed=False
        ))
        items.append(StudyPlanItem(
            study_plan_id=plan.id,
            topic_id=weak_topic.id,
            activity_type="Practice Diagnostic / Targeted Quiz",
            duration_minutes=time_quiz,
            priority="high",
            completed=False
        ))
    if next_topic and next_topic.id != (weak_topic.id if weak_topic else None):
        items.append(StudyPlanItem(
            study_plan_id=plan.id,
            topic_id=next_topic.id,
            activity_type="Explore Next Concept",
            duration_minutes=time_next,
            priority="medium",
            completed=False
        ))
    elif len(items) < 3 and topics:
        alt_topic = topics[-1]
        items.append(StudyPlanItem(
            study_plan_id=plan.id,
            topic_id=alt_topic.id,
            activity_type="Review & Revision",
            duration_minutes=time_next,
            priority="medium",
            completed=False
        ))

    for item in items:
        db.add(item)
    db.commit()
    db.refresh(plan)
    return plan
