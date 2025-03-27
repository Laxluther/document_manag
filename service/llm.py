import aiohttp
from loguru import logger
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ollamaUrl, ollamaModel

class LLM:
    
    @staticmethod
    async def answerGenerator(question, context):
       
        try:
            prompt = f"""
            You are a helpful assistant that answers questions based on the provided context.
            
            Context:
            {context}
            
            Question: {question}
            
            Answer the question based ONLY on the given context.
            If you don't have enough information, say "I don't have enough information to answer this question."
            
            Answer:
            """
            
            data = {
                "model": ollamaModel,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.3,
                "max_tokens": 512
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    ollamaUrl, 
                    json=data,
                    timeout=60
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("response", "").strip()
                    else:
                        error_text = await response.text()
                        logger.error(f"Ollama Error: {response.status} - {error_text}")
                        return "Error ollama"
                
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return "couldn't generate an answer."