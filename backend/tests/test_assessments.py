import pytest
import uuid
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def get_auth_token():
    unique_email = f"student_{uuid.uuid4().hex[:8]}@example.com"
    reg_res = client.post("/api/auth/register", json={
        "name": "Test Student",
        "email": unique_email,
        "password": "Password123!"
    })
    return reg_res.json()["access_token"]

def test_subjects_and_topics():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Test Subjects
    sub_res = client.get("/api/subjects", headers=headers)
    assert sub_res.status_code == 200
    subjects = sub_res.json()
    assert len(subjects) > 0
    dbms_id = subjects[0]["id"]

    # Test Topics
    topics_res = client.get(f"/api/subjects/{dbms_id}/topics", headers=headers)
    assert topics_res.status_code == 200
    topics = topics_res.json()
    assert len(topics) == 8  # 8 DBMS topics

    # Test Topic Details
    first_topic_id = topics[0]["id"]
    detail_res = client.get(f"/api/subjects/topics/{first_topic_id}", headers=headers)
    assert detail_res.status_code == 200
    assert len(detail_res.json()["materials"]) > 0

def test_diagnostic_and_quiz_flow():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch subjects
    sub_res = client.get("/api/subjects", headers=headers)
    dbms_id = sub_res.json()[0]["id"]

    # Get diagnostic questions
    diag_qs = client.get(f"/api/diagnostic/{dbms_id}/questions", headers=headers)
    assert diag_qs.status_code == 200
    qs_data = diag_qs.json()
    assert qs_data["total_questions"] > 0

    # Submit diagnostic
    answers = []
    for q in qs_data["questions"]:
        answers.append({
            "question_id": q["id"],
            "selected_answer": "B",
            "topic_id": q["topic_id"]
        })

    sub_diag = client.post("/api/diagnostic/submit", headers=headers, json={
        "subject_id": dbms_id,
        "answers": answers
    })
    assert sub_diag.status_code == 200
    diag_result = sub_diag.json()
    assert "overall_score" in diag_result
    assert "strong_topics" in diag_result
    assert "weak_topics" in diag_result

    # Generate topic quiz
    topics = client.get(f"/api/subjects/{dbms_id}/topics", headers=headers).json()
    topic_id = topics[0]["id"]

    gen_quiz = client.post("/api/quiz/generate", headers=headers, json={
        "topic_id": topic_id,
        "number_of_questions": 3,
        "difficulty": "medium"
    })
    assert gen_quiz.status_code == 200
    quiz_data = gen_quiz.json()
    assert len(quiz_data["questions"]) >= 1

    # Submit topic quiz
    quiz_answers = [{
        "question_id": q["id"],
        "selected_answer": "B",
        "response_time": 12
    } for q in quiz_data["questions"]]

    submit_quiz_res = client.post("/api/quiz/submit", headers=headers, json={
        "topic_id": topic_id,
        "difficulty": "medium",
        "answers": quiz_answers
    })
    assert submit_quiz_res.status_code == 200
    res_data = submit_quiz_res.json()
    assert "accuracy" in res_data
    assert "new_mastery" in res_data
    assert len(res_data["details"]) == len(quiz_answers)

    # Check dashboard reflection
    dash_res = client.get("/api/students/dashboard", headers=headers)
    assert dash_res.status_code == 200
    dash_data = dash_res.json()
    assert dash_data["student_name"] == "Test Student"
    assert dash_data["today_plan"] is not None
