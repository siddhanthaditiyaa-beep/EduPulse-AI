import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app.database.session import get_db
from backend.app.models.user import User
from backend.app.models.academic import Topic, Question
from backend.app.models.assessments import QuizAttempt, QuestionAttempt
from backend.app.models.performance import TopicPerformance
from backend.app.schemas.quiz import QuizGenerateRequest, QuizSubmitRequest, QuizResultResponse, QuestionResultDetail
from backend.app.auth.dependencies import get_current_user
from backend.app.services.mastery_service import calculate_topic_mastery
from backend.app.services.ai_service import ai_service
from backend.app.services.recommendation_service import generate_personalized_recommendations
from backend.app.services.study_plan_service import generate_daily_study_plan

router = APIRouter(prefix="/quiz", tags=["Quizzes & Assessments"])

@router.post("/generate")
def generate_quiz(
    data: QuizGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generates an adaptive quiz for a specific topic and difficulty.
    Mixes existing curated questions and AI-generated questions to ensure high fidelity.
    """
    topic = db.query(Topic).filter(Topic.id == data.topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Check existing questions in database
    existing_qs = db.query(Question).filter(Question.topic_id == topic.id).all()
    
    questions_to_serve = []

    # If we have enough existing questions for this topic, serve them
    if len(existing_qs) >= data.number_of_questions:
        selected_db_qs = existing_qs[:data.number_of_questions]
        for q in selected_db_qs:
            questions_to_serve.append({
                "id": q.id,
                "topic_id": q.topic_id,
                "question": q.question,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "difficulty": q.difficulty
            })
    else:
        # Generate new questions via AI service
        needed_count = data.number_of_questions - len(existing_qs)
        ai_generated = ai_service.generate_quiz_questions(
            topic_name=topic.name,
            difficulty=data.difficulty or "medium",
            count=max(needed_count, 3)
        )
        
        # Save newly generated questions to DB for permanence
        for ai_q in ai_generated:
            new_q = Question(
                topic_id=topic.id,
                question=ai_q["question"],
                option_a=ai_q["option_a"],
                option_b=ai_q["option_b"],
                option_c=ai_q["option_c"],
                option_d=ai_q["option_d"],
                correct_answer=ai_q["correct_answer"],
                explanation=ai_q["explanation"],
                difficulty=ai_q.get("difficulty", "medium")
            )
            db.add(new_q)
        db.commit()

        # Re-fetch from DB
        all_qs = db.query(Question).filter(Question.topic_id == topic.id).all()
        for q in all_qs[:data.number_of_questions]:
            questions_to_serve.append({
                "id": q.id,
                "topic_id": q.topic_id,
                "question": q.question,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "difficulty": q.difficulty
            })

    return {
        "topic_id": topic.id,
        "topic_name": topic.name,
        "difficulty": data.difficulty,
        "total_questions": len(questions_to_serve),
        "questions": questions_to_serve
    }

@router.post("/submit", response_model=QuizResultResponse)
def submit_quiz(
    data: QuizSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submits a completed quiz:
    - Calculates score and accuracy.
    - Records question-by-question attempts.
    - Recalculates topic mastery using the mathematical formula.
    - Awards XP and streak points.
    - Updates recommendations and study plan in real-time.
    """
    topic = db.query(Topic).filter(Topic.id == data.topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    total_questions = len(data.answers)
    if total_questions == 0:
        raise HTTPException(status_code=400, detail="Empty quiz submission")

    # Fetch prior mastery
    prior_perf = db.query(TopicPerformance).filter(
        TopicPerformance.user_id == current_user.id,
        TopicPerformance.topic_id == topic.id
    ).first()
    old_mastery = prior_perf.mastery_score if prior_perf else 0.0

    q_ids = [a.question_id for a in data.answers]
    questions_map = {q.id: q for q in db.query(Question).filter(Question.id.in_(q_ids)).all()}

    score = 0
    details = []

    for item in data.answers:
        q = questions_map.get(item.question_id)
        if not q:
            continue

        is_correct = (item.selected_answer.strip().upper() == q.correct_answer.strip().upper())
        if is_correct:
            score += 1

        details.append({
            "question_id": q.id,
            "question": q.question,
            "option_a": q.option_a,
            "option_b": q.option_b,
            "option_c": q.option_c,
            "option_d": q.option_d,
            "selected_answer": item.selected_answer,
            "correct_answer": q.correct_answer,
            "is_correct": is_correct,
            "explanation": q.explanation,
            "response_time": item.response_time
        })

    accuracy = round((score / total_questions) * 100.0, 1)

    # Save QuizAttempt
    attempt = QuizAttempt(
        user_id=current_user.id,
        topic_id=topic.id,
        score=score,
        total_questions=total_questions,
        accuracy=accuracy,
        difficulty=data.difficulty,
        completed_at=datetime.datetime.utcnow()
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    # Record granular QuestionAttempts
    for det in details:
        q_att = QuestionAttempt(
            quiz_attempt_id=attempt.id,
            question_id=det["question_id"],
            selected_answer=det["selected_answer"],
            is_correct=det["is_correct"],
            response_time=det["response_time"]
        )
        db.add(q_att)
    db.commit()

    # Recalculate topic mastery
    new_mastery = calculate_topic_mastery(
        user_id=current_user.id,
        topic_id=topic.id,
        db=db,
        new_attempt_accuracy=accuracy,
        new_attempt_difficulty=data.difficulty
    )

    # Calculate gamification XP
    xp_earned = (score * 15) + (25 if accuracy >= 80.0 else 0)
    if current_user.profile:
        current_user.profile.xp_points += xp_earned
        db.commit()

    # Update recommendations and daily study plan
    generate_personalized_recommendations(current_user.id, db)
    generate_daily_study_plan(current_user.id, db)

    return {
        "attempt_id": attempt.id,
        "topic_id": topic.id,
        "topic_name": topic.name,
        "score": score,
        "total_questions": total_questions,
        "accuracy": accuracy,
        "difficulty": data.difficulty,
        "xp_earned": xp_earned,
        "old_mastery": old_mastery,
        "new_mastery": new_mastery,
        "mistakes_count": total_questions - score,
        "details": details,
        "completed_at": attempt.completed_at
    }

@router.get("/history")
def get_quiz_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Fetch student's past quiz history."""
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == current_user.id
    ).order_by(QuizAttempt.completed_at.desc()).limit(20).all()

    topics_map = {t.id: t.name for t in db.query(Topic).all()}

    history = []
    for a in attempts:
        history.append({
            "id": a.id,
            "topic_id": a.topic_id,
            "topic_name": topics_map.get(a.topic_id, "Topic"),
            "score": a.score,
            "total_questions": a.total_questions,
            "accuracy": a.accuracy,
            "difficulty": a.difficulty,
            "completed_at": a.completed_at
        })
    return history
