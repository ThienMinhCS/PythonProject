import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "test123",
            "full_name": "Test User",
            "phone": "0912345678"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_user():
    response = client.post(
        "/auth/token",
        data={
            "username": "test@example.com",
            "password": "test123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()