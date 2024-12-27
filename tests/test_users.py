import pytest
from fastapi.testclient import TestClient
from app.core.security import get_password_hash

def test_create_user(client):
    response = client.post(
        "/api/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "Test123!@#"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "password" not in data

def test_create_user_invalid_password(client):
    response = client.post(
        "/api/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "weak"
        }
    )
    assert response.status_code == 422

def test_login(client, db):
    # Create a test user
    from app.models.user import User
    hashed_password = get_password_hash("Test123!@#")
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()

    response = client.post(
        "/api/users/login",
        data={
            "username": "testuser",
            "password": "Test123!@#"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer" 