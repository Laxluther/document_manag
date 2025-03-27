import os
from dotenv import load_dotenv

load_dotenv()


dbHost = os.getenv("dbHost", "localhost")
port = os.getenv("port", "5432")
dbName = os.getenv("dbName", "auraedu_data")
user_name = os.getenv("user_name", "postgres")
user_password = os.getenv("user_password", "postgres")


ollamaUrl = os.getenv("ollamaUrl", "http://localhost:11434/api/generate")
ollamaModel = os.getenv("ollamaModel", "llama3")

embeddingMod = os.getenv("embeddingMod", "sentence-transformers/all-MiniLM-L6-v2")


chunkSize = int(os.getenv("chunkSize", "1000"))
chunkOver = int(os.getenv("chunkOver", "200"))


langchain_splitter = os.getenv("langchain_splitter", "recursive")
langchain_LOADER = os.getenv("langchain_LOADER", "pypdf")


topK = int(os.getenv("topK", "3"))
simi_threshold= float(os.getenv("simi_threshold", "0.5"))