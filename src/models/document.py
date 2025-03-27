from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, JSON

from ..settings.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content = Column(Text, nullable=False)  
    is_selected = Column(Boolean, default=False)
    embeddings = relationship("Embedding", back_populates="document")

class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    vector = Column(JSON, nullable=False)  
    document = relationship("Document", back_populates="embeddings")
