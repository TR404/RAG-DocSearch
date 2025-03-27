import openai
import json 
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.document import Embedding



async def generate_embeddings(content: str) -> list[float]:
    """
    Generate embeddings for the given content using OpenAI's text-embedding-ada-002 model.
    """
    response = openai.Embedding.create(
        input=content,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

async def store_embeddings(document_id: int, content: str, db: AsyncSession):
    """
    Generate and store embeddings for a document in the database.
    """
    embeddings = await generate_embeddings(content)
    embedding_entry = Embedding(document_id=document_id, vector=embeddings)  
    db.add(embedding_entry)
    await db.commit()

async def retrieve_relevant_embeddings(question: str, db: AsyncSession, **kwargs) -> list[str]:
    """
    Retrieve relevant document embeddings for a given question.
    """
    question_embedding = await generate_embeddings(question)

    # Fetch all embeddings from the database with the related Document

    query = select(Embedding).options(joinedload(Embedding.document))
    document_ids = kwargs.get('document_ids')
    if document_ids:
        query = query.filter(Embedding.document_id.in_(document_ids))
    result = await db.execute(query)
    embeddings = result.scalars().all()

    relevant_embeddings = []
    for embedding in embeddings:
        embedding_vector = embedding.vector
        if isinstance(embedding_vector, str):
            embedding_vector = json.loads(embedding_vector)

        # Perform dot product to calculate similarity
        similarity = sum(q * e for q, e in zip(question_embedding, embedding_vector))  # Dot product
        if similarity > 0.5:  # Threshold for relevance
            if embedding.document:  # Ensure the document is not None
                relevant_embeddings.append(embedding.document.content)

    return relevant_embeddings

async def generate_answer(question: str, relevant_embeddings: list[str]) -> str:
    """
    Generate an answer using OpenAI's GPT model based on the question and relevant embeddings.
    """
    # Combine relevant embeddings into a single context
    context = "\n".join(relevant_embeddings)
    # Use OpenAI's GPT model to generate an answer
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can use "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ],
        max_tokens=200,  # Limit the response length
        temperature=0.7  # Adjust for creativity
    )

    # Extract and return the generated answer
    return response['choices'][0]['message']['content']