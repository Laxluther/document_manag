from sentence_transformers import SentenceTransformer
from loguru import logger
import numpy as np
from config import embeddingMod

class Embedding:
    
    model = None
    
    @classmethod
    def get_model(cls):
        if cls.model is None:
            logger.info(f"Loading model: {embeddingMod}")
            cls.model = SentenceTransformer(embeddingMod)
            logger.info("model loaded")
        return cls.model
    
    @classmethod
    async def generate_Embedding(cls, text):
       
        if not text or not text.strip():
            logger.warning("no text for embedding")
            return None
        model = cls.get_model()
        embedding = model.encode(text)
        return list(embedding)  
    
    @classmethod
    async def batchEmbeddings(cls, texts):
        if not texts:
            return []
        model = cls.get_model()
        embeddings = model.encode(texts)
        return [list(i) for i in embeddings] 
    
    @staticmethod
    async def calculate_cosine_similarity(embedding1, embedding2):
        x = np.array(embedding1)
        y = np.array(embedding2)
        
        dotProduct = np.dot(x, y)
        norm1 = np.linalg.norm(x)
        norm2 = np.linalg.norm(y)
        
     
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return float(dotProduct / (norm1 * norm2))