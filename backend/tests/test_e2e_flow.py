import uuid
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_complete_student_lifecycle_e2e():
    """
    End-to-End verification of the full student adaptive learning loop:
    Register -> Login -> Onboarding Profile -> Diagnostic Assessment ->
    Dashboard -> Study Session -> Quiz Generation -> Quiz Submit ->
    Mastery Update -> Prediction -> AI Tutor -> Study Plan Completion.
    """
    unique_email = f"e2e_student_{uuid.uuid4().hex[:6]}@university.edu"
    password = "SecurePassword123!"

    # 1. Register
    reg_res = client.post("/api/auth/register", json={
        "name": "Yuvraj Yadav",
        "email": unique_email,
        "password": password
    })
    assert reg_res.status_code == 201
    auth_data = reg_res.json()
    token = auth_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    assert auth_data["user"]["name"] == "Yuvraj Yadav"

    # 2. Login
    login_res = client.post("/api/auth/login", json={
        "email": unique_email,
        "password": password
    })
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()

    # 3. Update Profile (Onboarding)
    prof_res = client.put("/api/students/profile", headers=headers, json={
        "education_level": "Undergraduate (B.Tech CSE)",
        "learning_goal": "Semester Exam Preparation & Placement",
        "preferred_difficulty": "medium",
        "daily_study_target": 60
    })
    assert prof_res.status_code == 200
    assert prof_res.json()["daily_study_target"] == 60

    # 4. Fetch Subjects & Diagnostic Questions
    subs_res = client.get("/api/subjects", headers=headers)
    assert subs_res.status_code == 200
    dbms_id = subs_res.json()[0]["id"]

    diag_q_res = client.get(f"/api/diagnostic/{dbms_id}/questions", headers=headers)
    assert diag_q_res.status_code == 200
    questions = diag_q_res.json()["questions"]
    assert len(questions) > 0

    # 5. Submit Diagnostic Assessment
    diag_answers = [
        {"question_id": q["id"], "selected_answer": "B", "topic_id": q["topic_id"]}
        for q in questions
    ]
    diag_sub_res = client.post("/api/diagnostic/submit", headers=headers, json={
        "subject_id": dbms_id,
        "answers": diag_answers
    })
    assert diag_sub_res.status_code == 200
    diag_eval = diag_sub_res.json()
    assert "overall_score" in diag_eval
    assert diag_eval["initial_plan_generated"] is True

    # 6. Verify Dashboard State
    dash_res = client.get("/api/students/dashboard", headers=headers)
    assert dash_res.status_code == 200
    dash = dash_res.json()
    assert dash["student_name"] == "Yuvraj Yadav"
    assert dash["study_streak"] >= 1
    assert dash["today_plan"] is not None
    assert len(dash["today_plan"]["items"]) > 0

    # 7. Log Active Study Session
    first_topic_id = questions[0]["topic_id"]
    sess_res = client.post("/api/study-session/log", headers=headers, json={
        "topic_id": first_topic_id,
        "duration_minutes": 25,
        "completed_topic": True
    })
    assert sess_res.status_code == 200
    assert sess_res.json()["xp_earned"] >= 25

    # 8. Generate Adaptive Topic Quiz
    gen_quiz_res = client.post("/api/quiz/generate", headers=headers, json={
        "topic_id": first_topic_id,
        "difficulty": "medium",
        "number_of_questions": 3
    })
    assert gen_quiz_res.status_code == 200
    quiz_qs = gen_quiz_res.json()["questions"]
    assert len(quiz_qs) >= 1

    # 9. Submit Topic Quiz
    quiz_answers = [
        {"question_id": q["id"], "selected_answer": "B", "response_time": 15}
        for q in quiz_qs
    ]
    quiz_sub_res = client.post("/api/quiz/submit", headers=headers, json={
        "topic_id": first_topic_id,
        "difficulty": "medium",
        "answers": quiz_answers
    })
    assert quiz_sub_res.status_code == 200
    quiz_result = quiz_sub_res.json()
    assert "new_mastery" in quiz_result
    assert "details" in quiz_result

    # 10. Query AI Tutor with Mastery Awareness
    ai_res = client.post("/api/ai/tutor", headers=headers, json={
        "message": "Explain BCNF and how it differs from 3NF.",
        "topic_id": first_topic_id,
        "action_type": "explain_simply"
    })
    assert ai_res.status_code == 200
    tutor_reply = ai_res.json()
    assert "reply" in tutor_reply
    assert len(tutor_reply["reply"]) > 20

    # 11. Complete a Study Plan Item
    plan_item_id = dash["today_plan"]["items"][0]["id"]
    toggle_res = client.post(f"/api/study-plan/item/{plan_item_id}/toggle", headers=headers)
    assert toggle_res.status_code == 200
    assert toggle_res.json()["completed"] is True

    # 12. Check ML Prediction Endpoint
    pred_res = client.get("/api/performance/prediction", headers=headers)
    assert pred_res.status_code == 200
    pred_data = pred_res.json()
    assert "predicted_score" in pred_data
    assert "lower_bound" in pred_data
    assert "upper_bound" in pred_data

    # 13. Verify Performance Analytics & Knowledge Map
    perf_res = client.get("/api/performance?timeframe=30d", headers=headers)
    assert perf_res.status_code == 200
    perf_data = perf_res.json()
    assert len(perf_data["topics_mastery"]) == 8
    assert perf_data["total_quizzes_taken"] >= 1
