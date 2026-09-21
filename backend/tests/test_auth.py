import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_register_and_login():
    import uuid
    unique_email = f"student_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "name": "Yuvraj Yadav",
        "email": unique_email,
        "password": "Password123!"
    }
    
    # Test Registration
    reg_res = client.post("/api/auth/register", json=payload)
    assert reg_res.status_code == 201
    reg_data = reg_res.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["email"] == unique_email
    token = reg_data["access_token"]

    # Test Duplicate Registration Rejection
    dup_res = client.post("/api/auth/register", json=payload)
    assert dup_res.status_code == 400

    # Test Login
    login_res = client.post("/api/auth/login", json={
        "email": unique_email,
        "password": "Password123!"
    })
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()

    # Test Protected /auth/me
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["name"] == "Yuvraj Yadav"
