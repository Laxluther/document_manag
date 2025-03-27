from fastapi import APIRouter, HTTPException
from loguru import logger
from datetime import datetime

from service.rag import RAG
from .models import QuestionRequest, AnswerResponse, DocumentSelectionRequest, MessageResponse

router = APIRouter(prefix="/qa", tags=["qa"])

@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
  
    try:
        
        if not request.question or len(request.question.strip()) == 0:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
    
        answer = await RAG.answer_question(request.question)
        
        if not answer:
            raise HTTPException(status_code=500, detail="Failed to generate answer")
        
        return AnswerResponse(
            question=request.question,
            answer=answer,
            processed_at=datetime.now()
        )
        
    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")

@router.post("/documents", response_model=MessageResponse)
async def select_documents(request: DocumentSelectionRequest):
  
    try:
       
        if not request.document_ids:
            raise HTTPException(status_code=400, detail="Document IDs list cannot be empty")
        
       
        await RAG.doc_selection(request.document_ids)
        
        return MessageResponse(
            message=f"Selected {len(request.document_ids)} documents for Q&A"
        )
        
    except HTTPException as e:
        raise
    except Exception as e:
        logger.error(f"Error selecting documents: {e}")
        raise HTTPException(status_code=500, detail=f"Error selecting documents: {str(e)}")