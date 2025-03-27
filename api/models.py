from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class DocumentSelectionRequest(BaseModel):
    
    document_ids: List[int] = Field(..., description="List of document IDs to use for Q&A")

class QuestionRequest(BaseModel):
   
    question: str = Field(..., description="The question to answer")

class DocumentResponse(BaseModel):
    
    id: int
    filename: str
    file_type: str
    content_type: str
    created_at: datetime

class DocumentListResponse(BaseModel):
   
    documents: List[DocumentResponse]
    total: int

class AnswerResponse(BaseModel):
   
    question: str
    answer: str
    processed_at: datetime = Field(default_factory=datetime.now)

class MessageResponse(BaseModel):
  
    message: str
    success: bool = True