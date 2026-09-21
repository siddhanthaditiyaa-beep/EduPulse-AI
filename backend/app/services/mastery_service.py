from sqlalchemy.orm import Session
from backend.app.models.assessments import QuizAttempt
from backend.app.models.performance import TopicPerformance
import datetime

def get_mastery_level_label(score: float) -> str:
    """Map numeric mastery score (0-100) to standard pedagogical level."""
    if score >= 90.0:
        return "Mastered"
    elif score >= 75.0:
        return "Proficient"
    elif score >= 60.0:
        return "Developing"
    elif score >= 40.0:
        return "Needs Improvement"
    else:
        return "Beginner"

def calculate_topic_mastery(
    user_id: int,
    topic_id: int,
    db: Session,
    new_attempt_accuracy: float = None,
    new_attempt_difficulty: str = "medium"
) -> float:
    """
    Calculate an authentic mastery score between 0.0 and 100.0 based on real student performance.
    
    Formula:
    Mastery = 0.50 * WeightedAccuracy + 0.25 * DifficultyFactor + 0.15 * ExperienceFactor + 0.10 * ConsistencyBonus
    
    - WeightedAccuracy: Exponentially weights recent attempts higher than older ones.
    - DifficultyFactor: Scaling for attempting harder quizzes (Easy: 0.8, Medium: 1.0, Hard: 1.2).
    - ExperienceFactor: Caps at 5 completed quiz attempts to reward practice.
    - ConsistencyBonus: Rewards high accuracy (> 75%) across multiple attempts.
    """
    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == user_id,
        QuizAttempt.topic_id == topic_id
    ).order_by(QuizAttempt.completed_at.asc()).all()

    if not attempts:
        if new_attempt_accuracy is not None:
            return round(min(100.0, max(0.0, new_attempt_accuracy)), 1)
        return 0.0

    total_attempts = len(attempts)
    
    # 1. Weighted Accuracy (recent attempts get higher weight)
    weighted_acc_sum = 0.0
    weight_sum = 0.0
    for idx, att in enumerate(attempts):
        weight = 1.0 + (idx / total_attempts)  # older: 1.0, latest: ~2.0
        weighted_acc_sum += att.accuracy * weight
        weight_sum += weight
    avg_weighted_accuracy = weighted_acc_sum / weight_sum if weight_sum > 0 else 0.0

    # 2. Difficulty Factor
    diff_multipliers = {"easy": 0.85, "medium": 1.0, "hard": 1.15}
    diff_scores = [diff_multipliers.get(att.difficulty.lower(), 1.0) for att in attempts]
    avg_difficulty_multiplier = sum(diff_scores) / len(diff_scores) if diff_scores else 1.0

    # 3. Experience factor (0.0 to 1.0, saturates at 5 attempts)
    experience_factor = min(1.0, total_attempts / 5.0)

    # 4. Consistency bonus (if standard deviation is low or consecutive high scores)
    recent_attempts = attempts[-3:] if len(attempts) >= 3 else attempts
    recent_accuracies = [a.accuracy for a in recent_attempts]
    avg_recent = sum(recent_accuracies) / len(recent_accuracies)
    consistency_bonus = 10.0 if (avg_recent >= 75.0 and total_attempts >= 2) else (5.0 if avg_recent >= 60.0 else 0.0)

    # Combine into 0-100 mastery score
    base_mastery = (0.55 * avg_weighted_accuracy) + (0.20 * (avg_difficulty_multiplier * 100.0)) + (0.15 * (experience_factor * 100.0)) + (consistency_bonus)
    
    # Cap between 0 and 100
    final_mastery = round(max(0.0, min(100.0, base_mastery)), 1)

    # Update or insert into TopicPerformance table
    perf = db.query(TopicPerformance).filter(
        TopicPerformance.user_id == user_id,
        TopicPerformance.topic_id == topic_id
    ).first()

    avg_raw_accuracy = round(sum(a.accuracy for a in attempts) / total_attempts, 1)

    if perf:
        perf.accuracy = avg_raw_accuracy
        perf.mastery_score = final_mastery
        perf.attempts = total_attempts
        perf.last_updated = datetime.datetime.utcnow()
    else:
        perf = TopicPerformance(
            user_id=user_id,
            topic_id=topic_id,
            accuracy=avg_raw_accuracy,
            mastery_score=final_mastery,
            attempts=total_attempts,
            last_updated=datetime.datetime.utcnow()
        )
        db.add(perf)

    db.commit()
    db.refresh(perf)
    return final_mastery
