from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routers import auth, document, qa
from .settings.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield  


app = FastAPI(
    lifespan=lifespan,
    title="Shared Document Q&A System",
    description="""
Retrieval-Augmented Generation (RAG) Powered Document Q&A System:

- **Document Ingestion:**  
    Upload documents and generate embeddings for efficient retrieval.

- **Q&A API:**  
    Ask questions and get answers based on retrieved document embeddings.

- **Document Selection API:**  
    Select specific documents to refine the retrieval process.

- **Embeddings & Retrieval:**  
    Uses advanced vector search techniques (e.g., BM25, TF-IDF, LLM embeddings) for accurate document retrieval.
""",
    version="1.0.0",
)



app.include_router(auth.router, prefix="/v1")
app.include_router(document.router, prefix="/v1")
app.include_router(qa.router, prefix="/v1")


