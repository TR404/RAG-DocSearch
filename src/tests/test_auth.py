import pytest
import uuid
from fastapi.testclient import TestClient

from src.main import app

REGISTER_ENDPOINT = "/v1/auth/register"
LOGIN_ENDPOINT = "/v1/auth/token"
VALID_EMAIL = f"{uuid.uuid4()}@example.com"  # Generate a random email per test
VALID_PASSWORD = "SecurePass123"

@pytest.fixture(scope="module")
def client():
    """Fixture to provide a FastAPI test client."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.mark.asyncio
async def test_register(client):
    """Test user registration and handling of duplicate users."""

    # First registration attempt (should succeed)
    response = client.post(REGISTER_ENDPOINT, json={"email": VALID_EMAIL, "password": VALID_PASSWORD})
    assert response.status_code == 201
    assert response.json() == {"message": "User registered successfully"}

    # Second attempt with the same email (should fail)
    response_duplicate = client.post(REGISTER_ENDPOINT, json={"email": VALID_EMAIL, "password": VALID_PASSWORD})
    
    assert response_duplicate.status_code == 400
    assert response_duplicate.json() == {"detail": "User already registered"}

@pytest.mark.asyncio
async def test_login(client):
    """Test user login with valid and invalid credentials."""
    
    # Headers required for OAuth2 Password Grant
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    # Form-encoded login data
    data = {
        "grant_type": "password",
        "username": VALID_EMAIL,
        "password": VALID_PASSWORD,
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }
    response = client.post(LOGIN_ENDPOINT, data=data, headers=headers)
    
    assert response.status_code == 200, response.text
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"

    data["password"] = "InvalidPassword"
    invalid_response = client.post(LOGIN_ENDPOINT, data=data, headers=headers)
    
    assert invalid_response.status_code == 401, invalid_response.text
    assert invalid_response.json() == {"detail": "Invalid credentials"}
