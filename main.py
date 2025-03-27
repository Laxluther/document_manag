from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
from loguru import logger

from database.connection import init_database, close_pool
from service.embedding import Embedding
from api.doc_route import router as document_router
from api.qa import router as qa_router


logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("app.log", rotation="500 MB", level="INFO")

app = FastAPI(
    title="Document management & RAG QA api",
    description="Document management with rag-based question and answering",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document_router)
app.include_router(qa_router)

@app.on_event("startup")
async def startup():
    try:
        await init_database()
            
        i = Embedding.get_model()
        logger.info("Embedding model loaded successfully")
        
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        sys.exit(1)

@app.on_event("shutdown")
async def shutdown():
    await close_pool()
    logger.info("shut down")

@app.exception_handler(Exception)
async def globalException_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "error"}
    )

@app.get("/")
async def root():
    return {
        "message": "PDF management & rag QA api is running",
        "status": "OK",
        "docs_url": "/docs"
    }

# @app.get("/check")
# async def Check():
#     try:
#         if await test_connection():
#             if EmbeddingService._model is not None:
#                 return {
#                     "status": "healthy",
#                     "database": "connected",
#                     "embedding_model": "loaded"
#                 }
#             else:
#                 return {
#                     "status": "partial",
#                     "database": "connected", 
#                     "embedding_model": "not loaded"
#                 }
#         else:
#             return JSONResponse(
#                 status_code=503,
#                 content={
#                     "status": "unhealthy",
#                     "database": "disconnected"
#                 }
#             )
#     except Exception as e:
#         logger.error(f"Health check failed: {e}")
#         return JSONResponse(
#             status_code=503,
#             content={
#                 "status": "unhealthy",
#                 "message": str(e)
#             }
#         )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)