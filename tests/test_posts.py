import pytest
from fastapi.testclient import TestClient
from app.core.security import create_access_token
from app.models.user import User
from app.models.post import Post

@pytest.fixture
def test_user(db):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def token(test_user):
    return create_access_token({"sub": test_user.username})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

def test_create_post(authorized_client):
    response = authorized_client.post(
        "/api/posts/",
        json={
            "title": "Test Post",
            "content": "This is a test post content."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "This is a test post content."

def test_create_post_invalid_title(authorized_client):
    response = authorized_client.post(
        "/api/posts/",
        json={
            "title": "",  # Empty title
            "content": "This is a test post content."
        }
    )
    assert response.status_code == 422

def test_get_post(authorized_client, db, test_user):
    # Create a test post
    post = Post(
        title="Test Post",
        content="Test Content",
        author_id=test_user.id,
        vector_id="test-vector-id"
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    response = authorized_client.get(f"/api/posts/{post.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "Test Content"

def test_update_post(authorized_client, db, test_user):
    # Create a test post
    post = Post(
        title="Test Post",
        content="Test Content",
        author_id=test_user.id,
        vector_id="test-vector-id"
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    response = authorized_client.put(
        f"/api/posts/{post.id}",
        json={
            "title": "Updated Title",
            "content": "Updated Content"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated Content" 