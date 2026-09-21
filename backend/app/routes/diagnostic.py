import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.models.academic import Subject, Topic, Question
from backend.app.models.assessments import DiagnosticTest
from backend.app.models.performance import TopicPerformance
from backend.app.schemas.quiz import DiagnosticSubmitRequest, DiagnosticResultResponse
from backend.app.auth.dependencies import get_current_user
from backend.app.services.study_plan_service import generate_daily_study_plan
from backend.app.services.recommendation_service import generate_personalized_recommendations

router = APIRouter(prefix="/diagnostic", tags=["Diagnostic Assessment"])

@router.get("/{subject_id}/questions")
def get_diagnostic_questions(
    subject_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Fetches diagnostic assessment questions across all topics of a subject.
    Selects 1-2 representative questions per topic.
    """
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    diagnostic_questions = []
    for topic in subject.topics:
        # Take up to 2 questions from each topic
        topic_qs = db.query(Question).filter(Question.topic_id == topic.id).limit(2).all()
        for q in topic_qs:
            diagnostic_questions.append({
                "id": q.id,
                "topic_id": q.topic_id,
                "topic_name": topic.name,
                "question": q.question,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "difficulty": q.difficulty
            })

    return {
        "subject_id": subject.id,
        "subject_name": subject.name,
        "total_questions": len(diagnostic_questions),
        "questions": diagnostic_questions
    }

@router.post("/submit", response_model=DiagnosticResultResponse)
def submit_diagnostic_test(
    data: DiagnosticSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Evaluates diagnostic assessment:
    1. Calculates overall score.
    2. Calculates topic-wise accuracy.
    3. Identifies weak topics (< 60%) and strong topics (>= 75%).
    4. Initializes baseline topic mastery in database.
    5. Triggers initial personalized study plan generation.
    """
    subject = db.query(Subject).filter(Subject.id == data.subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    total_questions = len(data.answers)
    if total_questions == 0:
        raise HTTPException(status_code=400, detail="No answers provided for evaluation")

    correct_count = 0
    topic_stats = {}  # topic_id -> {"correct": int, "total": int, "name": str}

    # Fetch question database records
    q_ids = [a.question_id for a in data.answers]
    questions_map = {q.id: q for q in db.query(Question).filter(Question.id.in_(q_ids)).all()}
    topics_map = {t.id: t.name for t in subject.topics}

    for item in data.answers:
        q = questions_map.get(item.question_id)
        if not q:
            continue
        t_id = q.topic_id
        if t_id not in topic_stats:
            topic_stats[t_id] = {"correct": 0, "total": 0, "name": topics_map.get(t_id, "Topic")}

        topic_stats[t_id]["total"] += 1
        is_correct = (item.selected_answer.strip().upper() == q.correct_answer.strip().upper())
        if is_correct:
            correct_count += 1
            topic_stats[t_id]["correct"] += 1

    overall_percentage = round((correct_count / total_questions) * 100.0, 1)

    # Save diagnostic test record
    diag = DiagnosticTest(
        user_id=current_user.id,
        subject_id=subject.id,
        score=overall_percentage,
        completed_at=datetime.datetime.utcnow()
    )
    db.add(diag)

    # Calculate topic breakdown & initialize topic mastery
    topic_breakdown = []
    strong_topics = []
    weak_topics = []

    for t_id, stats in topic_stats.items():
        acc = round((stats["correct"] / stats["total"]) * 100.0, 1) if stats["total"] > 0 else 0.0
        # Initialize mastery score directly from diagnostic baseline
        initial_mastery = round(acc * 0.9, 1)

        topic_breakdown.append({
            "topic_id": t_id,
            "topic_name": stats["name"],
            "correct": stats["correct"],
            "total": stats["total"],
            "accuracy": acc,
            "initial_mastery": initial_mastery
        })

        if acc >= 75.0:
            strong_topics.append(stats["name"])
        elif acc < 60.0:
            weak_topics.append(stats["name"])

        # Update or create TopicPerformance
        perf = db.query(TopicPerformance).filter(
            TopicPerformance.user_id == current_user.id,
            TopicPerformance.topic_id == t_id
        ).first()

        if perf:
            perf.accuracy = acc
            perf.mastery_score = initial_mastery
            perf.attempts = max(1, perf.attempts)
            perf.last_updated = datetime.datetime.utcnow()
        else:
            perf = TopicPerformance(
                user_id=current_user.id,
                topic_id=t_id,
                accuracy=acc,
                mastery_score=initial_mastery,
                attempts=1,
                last_updated=datetime.datetime.utcnow()
            )
            db.add(perf)

    # Award XP for completing diagnostic test
    if current_user.profile:
        current_user.profile.xp_points += 100
        # Add badge
        current_user.profile.badges_json = '["Welcome Pioneer", "Diagnostic Pioneer"]'

    db.commit()

    # Generate initial personalized study plan and recommendations
    generate_personalized_recommendations(current_user.id, db)
    generate_daily_study_plan(current_user.id, db)

    return {
        "test_id": diag.id,
        "subject_id": subject.id,
        "subject_name": subject.name,
        "overall_score": overall_percentage,
        "total_questions": total_questions,
        "correct_answers": correct_count,
        "topic_breakdown": topic_breakdown,
        "strong_topics": strong_topics,
        "weak_topics": weak_topics,
        "initial_plan_generated": True,
        "completed_at": diag.completed_at
    }
