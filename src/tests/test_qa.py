import pytest
from fastapi.testclient import TestClient

from src.main import app

ASK_ENDPOINT = "/v1/qa/ask"
VALID_QUESTION = "should i need to use background task"
VALID_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaGl2YW0udGl3YXJpQGdtYWlsLmNvbSIsImV4cCI6MTc0MzA3Mjg3NX0.84jOzsSoNqhGZpr5NbH2Vp1RWQjkFB66N2SQwePpXw4"

@pytest.fixture(scope="module")
def client():
    """Fixture to provide a FastAPI test client."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.mark.blocking  # Mark this test as synchronous
def test_question_answering(client):
    """Test the /ask endpoint with a valid question and token."""
    
    # Headers with Authorization token
    headers = {
        "Authorization": VALID_TOKEN,
        "accept": "application/json" 
    }
    
    # Sending a POST request to the /ask endpoint
    response = client.post(f"{ASK_ENDPOINT}?question={VALID_QUESTION}", headers=headers)
    
    # Assert the response status code
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Response: {response.text}"
    
    # Assert the response JSON structure
    json_response = response.json()
    assert "question" in json_response, f"Missing 'question' in response: {json_response}"
    assert "answer" in json_response, f"Missing 'answer' in response: {json_response}"
    assert json_response["question"] == VALID_QUESTION, f"Unexpected question: {json_response['question']}"
    assert isinstance(json_response["answer"], str), f"Answer is not a string: {json_response['answer']}"