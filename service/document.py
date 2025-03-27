import os
import tempfile
import sys
from loguru import logger
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import chunkSize, chunkOver

class Processor:
    
    @staticmethod
    async def doc_process(file_content, file_type):
        if file_type.lower() != 'pdf':
            raise ValueError(f"Only PDF are supported. Got: {file_type}")
      
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_file.write(file_content)
        temp_file.close()
        temp_file_path = temp_file.name

        loader = PyPDFLoader(temp_file_path)
        documents = loader.load()
        
        os.unlink(temp_file_path)
        
       
        if not documents:
            logger.warning("No content")
            return []
       
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunkSize,
            chunk_overlap=chunkOver,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        
     
        result = [(i, chunk.page_content) for i, chunk in enumerate(chunks)]
        
        logger.info(f"PDF Processed into {len(result)} chunks")
        return result