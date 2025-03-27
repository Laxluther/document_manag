import asyncpg
import sys
import os
from loguru import logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import dbHost, port, dbName, user_name, user_password

pool = None

async def get_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(
            host=dbHost,
            port=port,
            database=dbName,
            user=user_name,
            password=user_password,
            min_size=3,
            max_size=10
        )
    return pool

async def init_database():
    logger.info("Initializing database...")
    
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            file_type VARCHAR(50) NOT NULL,
            content_type VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id SERIAL PRIMARY KEY,
            document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
            chunk_text TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            chunk_embedding BYTEA,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (document_id, chunk_index)
        )
        """)
        
      
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS document_selections (
            id SERIAL PRIMARY KEY,
            document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (document_id)
        )
        """)

async def close_pool():
    global pool
    if pool:
        await pool.close()
        pool = None
        logger.info("pool closed")

# async def test_connection():
#     try:
#         pool = await get_pool()
#         async with pool.acquire() as conn:
#             version = await conn.fetchval("SELECT version()")
#             logger.info(f"Connected to PostgreSQL: {version}")
#             return True
#     except Exception as e:
#         logger.error(f"Connection test failed: {e}")
#         return False