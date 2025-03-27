from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException

from ..settings.database import get_db
from ..models.document import Document
from ..services.text_extraction import extract_text
from ..services.validate_token import get_current_user
from ..services.openai_service import store_embeddings

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    Upload a document, save it to the database, and generate embeddings for it.
    """
    try:
        # Read the file content
        binary_content = await file.read()

        # Extract text based on file type
        try:
            extracted_text = extract_text(file.content_type.split("/")[-1], binary_content)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to extract text: {str(e)}")

        # Save the extracted text to the database
        doc = Document(filename=file.filename, content=extracted_text)  # Save extracted text
        db.add(doc)
        await db.commit()

        # Generate and store embeddings for the extracted text
        await store_embeddings(document_id=doc.id, content=extracted_text, db=db)

        return {"message": "Upload successful", "document_id": doc.id}
    except Exception as e:
        return {"error": str(e)}



@router.post("/selection")
async def select_documents(
    document_ids: List[int], 
    db: AsyncSession = Depends(get_db), 
    current_user: str = Depends(get_current_user)
):
    """
    Document Selection API: Allows users to specify which documents to include
    in the Q&A process.
    """
    try:
        # Fetch documents using async query
        result = await db.execute(select(Document).filter(Document.id.in_(document_ids)))
        documents = result.scalars().all()

        if not documents:
            raise HTTPException(status_code=404, detail="No documents found with the given IDs.")

        # Mark selected documents
        for doc in documents:
            doc.is_selected = True

        await db.commit()

        return {"message": "Documents selected successfully.", "selected_documents": [doc.id for doc in documents]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))