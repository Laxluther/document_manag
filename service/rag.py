from loguru import logger
from .document import Processor
from .embedding import Embedding
from .llm import LLM
from database.operations import DatabaseOperation
from config import topK

class RAG:
    
    @staticmethod
    async def processStore_document(file_content, filename, file_type, content_type):
      
        chunks = await Processor.doc_process(file_content, file_type)
        
        if not chunks:
            logger.warning(f"No text chunks extracted from {filename}")
            return None
        
        logger.info(f"Extracted {len(chunks)} chunks from {filename}")
        
        document_id = await DatabaseOperation.insert_doc(
            filename, file_type, content_type
        )
      
        chunk_text = [chunk[1] for chunk in chunks]
        embeddings = await Embedding.batchEmbeddings(chunk_text)
       
        for (chunk_index, chunk_text), embedding in zip(chunks, embeddings):
            await DatabaseOperation.insert_chunk(
                document_id, chunk_text, chunk_index, embedding
            )
        
        logger.info(f"Document {filename} processed and stored with ID: {document_id}")
        return document_id
    
    @staticmethod
    async def doc_selection(document_ids):
       
        await DatabaseOperation.doc_selection(document_ids)
        logger.info(f"Selected {len(document_ids)} documents for Q&A")
    
    @staticmethod
    async def answer_question(question):
        
        question_embedding = await Embedding.generate_Embedding(question)
        
        if not question_embedding:
            logger.warning("Could not generate embedding")
            return "I couldn't process your question."
       
        similar_chunks = await DatabaseOperation.similar_chunks_search(
            question_embedding, topK
        )
        
        if not similar_chunks:
            logger.warning("No relevant chunks found")
            return "No relevant information in the documents."
       
        context = "\n\n".join([chunk['chunk_text'] for chunk in similar_chunks])
        
        answer = await LLM.answerGenerator(question, context)
     
        sources = [f"- {chunk['filename']} (Similarity: {chunk['rank']:.4f})" for chunk in similar_chunks]
        sources_text = "\n".join(sources)
        
        full_answer = f"{answer}\n\nSources:\n{sources_text}"
        
        return full_answer