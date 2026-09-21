from sqlalchemy.orm import Session
from backend.app.models.academic import Topic, Subject
from backend.app.models.performance import TopicPerformance
from backend.app.models.recommendations import Recommendation
from backend.app.models.assessments import QuizAttempt
import datetime

def generate_personalized_recommendations(user_id: int, db: Session) -> list:
    """
    Analyzes student's actual performance data and generates grounded recommendations.
    Rules:
    1. Weak Topics (< 60% mastery) -> Priority: High (Revision & targeted practice)
    2. Unattempted Topics -> Priority: Medium (New topic study)
    3. Moderate Mastery (60-75%) -> Priority: Medium (Advanced practice quiz)
    4. Strong Mastery (> 85%) -> Retention / Mastery reinforcement
    """
    # Remove older incomplete recommendations to keep them fresh
    db.query(Recommendation).filter(
        Recommendation.user_id == user_id,
        Recommendation.completed == False
    ).delete()
    db.commit()

    # Query all topics and student's performance
    topics = db.query(Topic).order_by(Topic.order_index.asc()).all()
    performances = {p.topic_id: p for p in db.query(TopicPerformance).filter(TopicPerformance.user_id == user_id).all()}

    new_recommendations = []

    for topic in topics:
        perf = performances.get(topic.id)
        if not perf or perf.attempts == 0:
            # Unattempted topic
            rec = Recommendation(
                user_id=user_id,
                topic_id=topic.id,
                recommendation_type="new_topic",
                priority="medium",
                reason=f"You haven't attempted '{topic.name}' yet. Review the core concepts and take an introductory quiz.",
                completed=False,
                created_at=datetime.datetime.utcnow()
            )
            new_recommendations.append(rec)
        elif perf.mastery_score < 50.0:
            # Critical weakness
            rec = Recommendation(
                user_id=user_id,
                topic_id=topic.id,
                recommendation_type="focus_weakness",
                priority="high",
                reason=f"Your mastery in '{topic.name}' is currently {perf.mastery_score:.0f}% with an accuracy of {perf.accuracy:.0f}%. Re-study fundamentals and solve practice questions.",
                completed=False,
                created_at=datetime.datetime.utcnow()
            )
            new_recommendations.append(rec)
        elif perf.mastery_score < 70.0:
            # Developing
            rec = Recommendation(
                user_id=user_id,
                topic_id=topic.id,
                recommendation_type="practice_quiz",
                priority="medium",
                reason=f"You're making steady progress in '{topic.name}' ({perf.mastery_score:.0f}%). Take a medium-difficulty quiz to push to proficient level.",
                completed=False,
                created_at=datetime.datetime.utcnow()
            )
            new_recommendations.append(rec)

    # Sort so high priority comes first
    priority_order = {"high": 1, "medium": 2, "low": 3}
    new_recommendations.sort(key=lambda r: priority_order.get(r.priority, 4))

    # Keep top 5 to avoid overwhelming the student
    selected = new_recommendations[:5]
    for r in selected:
        db.add(r)
    db.commit()

    return db.query(Recommendation).filter(
        Recommendation.user_id == user_id,
        Recommendation.completed == False
    ).all()
