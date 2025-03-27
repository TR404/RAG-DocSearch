from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends

from ..settings.database import get_db
from ..services.validate_token import get_current_user
from src.services.openai_service import generate_answer, retrieve_relevant_embeddings

router = APIRouter(prefix="/qa", tags=["Q&A"])

@router.post("/ask")
async def question_answering(question: str, document_ids: Optional[List[int]] = None, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    """
    Q&A API: Accepts a user question, retrieves relevant document embeddings,
    and generates an answer using OpenAI GPT.
    """
    try:
        # Retrieve relevant embeddings
        relevant_embeddings = await retrieve_relevant_embeddings(question, db, document_ids=document_ids)

        if not relevant_embeddings:
            raise HTTPException(status_code=404, detail="No relevant documents found.")

        # Generate answer using OpenAI GPT
        answer = await generate_answer(question, relevant_embeddings)
        return {"question": question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))