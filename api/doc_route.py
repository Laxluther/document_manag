from fastapi import APIRouter, UploadFile, File, HTTPException
from loguru import logger

from service.rag import RAG
from database.operations import DatabaseOperation
from .models import DocumentListResponse, DocumentResponse, MessageResponse

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", response_model=MessageResponse)
async def upload_document(file: UploadFile = File(...)):
    try:
        content_type = file.content_type
        filename = file.filename
        
        
        if "pdf" in content_type or filename.lower().endswith(".pdf"):
            file_type = "pdf"
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Only PDF files are supported. Got: {content_type}"
            )
        
       
        file_content = await file.read()
        
        if not file_content:
            raise HTTPException(status_code=400, detail="Empty file")
        
       
        document_id = await RAG.processStore_document(
            file_content, 
            filename, 
            file_type, 
            content_type
        )
        
        if not document_id:
            raise HTTPException(status_code=500, detail="Failed to process document")
            
        return MessageResponse(
            message=f"PDF document uploaded and processed successfully with ID: {document_id}"
        )
        
    except HTTPException as e:
       
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@router.get("/", response_model=DocumentListResponse)
async def get_documents():
   
    try:
        documents = await DatabaseOperation.get_all_docs()
        
        # Convert to response models
        document_responses = []
        for doc in documents:
            document_responses.append(DocumentResponse(
                id=doc['id'],
                filename=doc['filename'],
                file_type=doc['file_type'],
                content_type=doc['content_type'],
                created_at=doc['created_at']
            ))
        
        return DocumentListResponse(
            documents=document_responses,
            total=len(document_responses)
        )
        
    except Exception as e:
        logger.error(f"Error getting documents: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting documents: {str(e)}")