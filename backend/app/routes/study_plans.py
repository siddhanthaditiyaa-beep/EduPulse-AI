from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.models.study import StudyPlan, StudyPlanItem
from backend.app.models.academic import Topic
from backend.app.auth.dependencies import get_current_user
from backend.app.services.study_plan_service import generate_daily_study_plan

router = APIRouter(prefix="/study-plan", tags=["Personalized Study Plan"])

@router.get("")
def get_daily_study_plan(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetch or generate the student's personalized daily plan."""
    plan = generate_daily_study_plan(current_user.id, db)
    topics_map = {t.id: t.name for t in db.query(Topic).all()}

    items_list = []
    completed_count = 0
    for it in plan.items:
        if it.completed:
            completed_count += 1
        items_list.append({
            "id": it.id,
            "topic_id": it.topic_id,
            "topic_name": topics_map.get(it.topic_id, "Topic"),
            "activity_type": it.activity_type,
            "duration_minutes": it.duration_minutes,
            "priority": it.priority,
            "completed": it.completed
        })

    progress_pct = round((completed_count / len(items_list)) * 100.0) if items_list else 0

    return {
        "id": plan.id,
        "title": plan.title,
        "description": plan.description,
        "duration": plan.duration,
        "progress_percentage": progress_pct,
        "completed_count": completed_count,
        "total_count": len(items_list),
        "items": items_list
    }

@router.post("/item/{item_id}/toggle")
def toggle_study_plan_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a study plan activity item as completed or pending."""
    item = db.query(StudyPlanItem).join(StudyPlan).filter(
        StudyPlanItem.id == item_id,
        StudyPlan.user_id == current_user.id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Study plan item not found")

    item.completed = not item.completed
    if item.completed and current_user.profile:
        current_user.profile.xp_points += 20  # XP for finishing an item

    db.commit()
    return {"id": item.id, "completed": item.completed, "status": "success"}
