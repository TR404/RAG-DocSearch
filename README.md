# Python Backend Project for Document Ingestion and RAG-based Q&A

This project is a Python-based backend application designed for document ingestion and retrieval-based Q&A (RAG). It utilizes a Large Language Model (LLM) for embedding generation and provides APIs for document ingestion, question answering, and document selection.

## Project Overview

The application is designed to manage users, documents, and an ingestion process that generates embeddings for document retrieval in a Q&A setting. It uses OpenAI's API for embedding generation and PostgreSQL for storing embeddings. The backend is built with FastAPI and supports asynchronous programming for efficient API handling.

## Key Features

1. **Document Ingestion API**:
   - Accepts document data.
   - Generates embeddings using OpenAI's API.
   - Stores embeddings in a PostgreSQL database.

2. **Q&A API**:
   - Accepts user questions.
   - Retrieves relevant document embeddings.
   - Generates answers using a Retrieval-Augmented Generation (RAG) approach.

3. **Document Selection API**:
   - Enables users to specify which documents to consider in the RAG-based Q&A process.

## Project Structure

```
RAG-DocSearch
├── src
│   ├── main.py                  # Entry point of the RAG-DocSearch application
│   ├── models
│   │   └── document.py          # Database models for document ingestion and retrieval
│   │   └── user.py              # Database models for user management
│   ├── routers
│   │   └── auth.py              # API endpoints for user authentication and authorization
│   │   └── document.py          # API endpoints for document ingestion and selection
│   │   └── qa.py                # API endpoints for Q&A functionality
│   ├── schemas
│   │   └── document.py          # Pydantic schemas for document-related requests and responses
│   │   └── user.py              # Pydantic schemas for user-related requests and responses
│   ├── services
│   │   └── auth.py              # Business logic for authentication and token management
│   │   └── openai_service.py    # Integration with OpenAI API for embedding generation
│   │   └── text_extraction.py   # Logic for extracting text from documents
│   │   └── validate_token.py    # Token validation and utility functions
│   ├── settings
│   │   └── base.py              # Application configuration and environment settings
│   │   └── database.py          # Database connection and initialization logic
│   └── tests
│       └── test_auth.py         # Unit tests for authentication functionality
│       └── test_main.py         # Unit tests for the main application
│       └── test_qa.py           # Unit tests for Q&A functionality
├── Dockerfile                    # Instructions to build the Docker image for the application
├── docker-compose.yml            # Configuration for running multi-container Docker applications
├── requirements.txt              # List of Python dependencies for the project
├── README.md                     # Documentation for the RAG-DocSearch project
└── .github
    └── workflows
        └── ci-cd.yml            # CI/CD pipeline configuration for automated testing and deployment
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TR404/RAG-DocSearch.git
   cd RAG-DocSearch
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   uvicorn src.app:app --host 0.0.0.0 --port 8000
   ```

4. **Access the APIs:**
   - User Registration API: `/v1/auth/register` (Registers a new user)
   - Document Ingestion API: `/v1/documents/ingest` (Accepts document data and generates embeddings)
   - Document Selection API: `/v1/documents/selection` (Allows users to specify documents for Q&A)
   - Q&A API: `/v1/qa/ask` (Accepts user questions and retrieves answers using RAG)

## API Usage

### **Document Ingestion API**
- **Method**: POST
- **Endpoint**: `/v1/documents/ingest`
- **Body**: JSON containing document data.

### **Q&A API**
- **Method**: POST
- **Endpoint**: `/v1/qa/ask`
- **Body**: JSON containing the user question.

### **Document Selection API**
- **Method**: POST
- **Endpoint**: `/v1/documents/selection`
- **Body**: JSON specifying document selection criteria.

### **User Registration API**
- **Method**: POST
- **Endpoint**: `/v1/auth/register`
- **Body**: JSON containing user registration details.
  ```json
  {
      "email": "example_user",
      "password": "example_password"
  }
  ```

## Development Guidelines

- Follow best practices for code quality and maintainability.
- Ensure asynchronous programming practices are implemented for performance.
- Write unit tests for all new features and maintain a test coverage of 70% or higher.
- Document all code and provide comprehensive design documentation.

## Deployment

1. **Dockerization**:
   - The project includes a `Dockerfile` and `docker-compose.yml` for containerization.
   - To build and run the application using Docker:
     ```bash
     docker-compose up --build
     ```

2. **CI/CD Pipeline**:
   - The project includes a GitHub Actions workflow (`.github/workflows/ci-cd.yml`) for automating testing, building, and deployment.

## Non-Functional Aspects

- **Performance**: Asynchronous programming ensures efficient handling of API requests.
- **Scalability**: The application is designed to handle large datasets and high query volumes.
- **Security**: Future improvements include HTTPS, authentication, and authorization.

## Testing

- The project uses `pytest` and `pytest-asyncio` for unit testing.
- Test coverage is targeted at 70% or higher.
- Tests include positive and negative workflows for all APIs.

## Future Improvements

1. **Caching**: Implement Redis for caching embeddings and answers to reduce latency.
2. **Scaling**: Use Celery with Redis for distributed task queues and batch processing.
3. **Monitoring**: Add logging and monitoring tools like Sentry or Prometheus.
4. **Deployment**: Add Kubernetes deployment scripts for cloud providers.

## Contact

For any questions or issues, please contact the project maintainer.