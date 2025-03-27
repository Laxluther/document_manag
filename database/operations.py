import json
from .connection import get_pool
from config import topK
from service.embedding import Embedding

class DatabaseOperation:
    
    @staticmethod
    async def insert_doc(filename, file_type, content_type):
        pool = await get_pool()
        async with pool.acquire() as conn:
            document_id = await conn.fetchval(
                """
                INSERT INTO documents (filename, file_type, content_type)
                VALUES ($1, $2, $3)
                RETURNING id
                """,
                filename, file_type, content_type
            )
            return document_id
          
    @staticmethod
    async def insert_chunk(document_id, chunk_text, chunk_index, embedding=None):
        pool = await get_pool()
        async with pool.acquire() as conn:
            binary_embedding = None
            if embedding is not None:
                embedding_list = [float(x) for x in embedding]
                binary_embedding = json.dumps(embedding_list).encode('utf-8')
            
            await conn.execute(
                """
                INSERT INTO document_chunks 
                    (document_id, chunk_text, chunk_index, chunk_embedding)
                VALUES 
                    ($1, $2, $3, $4)
                """,
                document_id, chunk_text, chunk_index, binary_embedding
            )
    
    @staticmethod
    async def get_doc(document_id):
        
        pool = await get_pool()
        async with pool.acquire() as conn:
            return await conn.fetchrow(
                "SELECT * FROM documents WHERE id = $1",
                document_id
            )
    
    @staticmethod
    async def get_all_docs():
       
        pool = await get_pool()
        async with pool.acquire() as conn:
            return await conn.fetch(
                "SELECT * FROM documents ORDER BY created_at DESC"
            )
    
    @staticmethod
    async def doc_selection(document_ids):
        
        pool = await get_pool()
        async with pool.acquire() as conn:
            async with conn.transaction():
               
                await conn.execute("DELETE FROM document_selections")
                
               
                for doc_id in document_ids:
                    await conn.execute(
                        """
                        INSERT INTO document_selections (document_id)
                        VALUES ($1)
                        """,
                        doc_id
                    )
    
    @staticmethod
    async def get_selected_doc():
        pool = await get_pool()
        async with pool.acquire() as conn:
            return await conn.fetch(
                """
                SELECT d.* FROM documents d
                JOIN document_selections ds ON d.id = ds.document_id
                """
            )
    
    @staticmethod
    async def similar_chunks_search(query_embedding, limit=topK):
      
        pool = await get_pool()
        async with pool.acquire() as conn:
            selected_docs = await conn.fetch("SELECT document_id FROM document_selections")
            
         
            doc_filter = ""
            params = []
            
            if selected_docs:
                doc_ids = [row['document_id'] for row in selected_docs]
                placeholders = ','.join(f'${i+1}' for i in range(len(doc_ids)))
                doc_filter = f"WHERE dc.document_id IN ({placeholders})"
                params = doc_ids
        
            query = f"""
            SELECT 
                dc.id, 
                dc.chunk_text, 
                dc.document_id, 
                d.filename, 
                dc.chunk_embedding
            FROM document_chunks dc
            JOIN documents d ON dc.document_id = d.id
            {doc_filter}
            """
            
            chunks = await conn.fetch(query, *params)
            
            similarities = []
            for chunk in chunks:
                if chunk['chunk_embedding'] is None:
                    continue
                    
                chunk_embedding = json.loads(chunk['chunk_embedding'].decode('utf-8'))
                
                similarity = await Embedding.calculate_cosine_similarity(
                    query_embedding, chunk_embedding
                )
             
                if similarity > 0:
                    similarities.append({
                        'id': chunk['id'],
                        'chunk_text': chunk['chunk_text'],
                        'document_id': chunk['document_id'],
                        'filename': chunk['filename'],
                        'rank': similarity
                    })
                
            similarities.sort(key=lambda x: x['rank'], reverse=True)
            return similarities[:limit]