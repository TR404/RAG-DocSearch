import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.main import app

VALID_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaGl2YW0udGl3YXJpQGdtYWlsLmNvbSIsImV4cCI6MTc0MzA3Mjg3NX0.84jOzsSoNqhGZpr5NbH2Vp1RWQjkFB66N2SQwePpXw4"

@pytest.fixture(scope="module")
def client():
    """Fixture to provide a FastAPI test client."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def mock_db():
    """Mock AsyncSession for testing database interactions."""
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def mock_get_current_user():
    """Mock dependency for getting the current user."""
    return "test_user"

@pytest.mark.asyncio
async def test_ingest_document(client, mock_db, mock_get_current_user):
    """Test document ingestion endpoint."""
    headers = {"Authorization": VALID_TOKEN}
    files = {"file": ("test.txt", b"Sample text content", "text/plain")}
    
    response = client.post("v1/documents/ingest", headers=headers, files=files)
    
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    json_response = response.json()
    assert "message" in json_response, "Missing 'message' in response"
    assert json_response["message"] == "Upload successful"
    assert "document_id" in json_response, "Missing 'document_id' in response"

@pytest.mark.asyncio
async def test_select_documents(client, mock_db, mock_get_current_user):
    """Test document selection endpoint."""
    headers = {"Authorization": VALID_TOKEN, "accept": "application/json"}
    data = {"document_ids": [1, 2, 3]}
    
    response = client.post("v1/documents/selection", headers=headers, json=data)
    
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    json_response = response.json()
    assert "message" in json_response, "Missing 'message' in response"
    assert json_response["message"] == "Documents selected successfully."
    assert "selected_documents" in json_response, "Missing 'selected_documents' in response"
    assert isinstance(json_response["selected_documents"], list), "'selected_documents' should be a list"
