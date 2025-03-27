# Document Management & RAG-based Q&A API

Welcome to our Document Management and RAG-based Question & Answering application! This tool helps you manage documents and get intelligent answers from your document library.

## Features

- **Document Upload**: Easily upload PDF documents into the system
- **Smart Document Processing**: Your documents are automatically processed into chunks and indexed for efficient retrieval
- **Powerful Q&A**: Ask questions in natural language and get answers based on your uploaded documents
- **Document Selection**: Choose which documents to include in the knowledge base for answering questions

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Ollama (for LLM capabilities)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-repo/document-qa-system.git
cd document-qa-system
```

2. **Set up environment**

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. **Configure environment variables**

Create a `.env` file in the root directory with the following variables:

```
# Database settings
dbHost=localhost
port=5432
dbName=auraedu_data
user_name=postgres
user_password=postgres

# LLM settings
ollamaUrl=http://localhost:11434/api/generate
ollamaModel=llama3

# Embedding settings
embeddingMod=sentence-transformers/all-MiniLM-L6-v2

# Document processing settings
chunkSize=1000
chunkOver=200
topK=3
simi_threshold=0.5
```

4. **Start the application**

```bash
uvicorn main:app --reload
```

Your API will be running at http://localhost:8000. Visit http://localhost:8000/docs for the Swagger UI documentation.

## How to Use the API

### 1. Upload Documents

Upload your PDF files to make them available for querying.

```bash
curl -X 'POST' \
  'http://localhost:8000/documents/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_document.pdf'
```

Or use the Swagger UI at `/docs` to upload files through the browser.

### 2. List Available Documents

View all documents that have been uploaded to the system.

```bash
curl -X 'GET' \
  'http://localhost:8000/documents/' \
  -H 'accept: application/json'
```

### 3. Select Documents for Q&A

Choose which documents to include in the knowledge base for answering questions.

```bash
curl -X 'POST' \
  'http://localhost:8000/qa/documents' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "document_ids": [1, 2]
}'
```

### 4. Ask Questions

Now you can ask questions about your documents!

```bash
curl -X 'POST' \
  'http://localhost:8000/qa/ask' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "What are the key concepts in chapter 3?"
}'
```

## Examples

**Example 1: Upload a document**
```bash
curl -X 'POST' \
  'http://localhost:8000/documents/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@statistics_textbook.pdf'
```

Response:
```json
{
  "message": "PDF document uploaded and processed successfully with ID: 1",
  "success": true
}
```

**Example 2: Select documents for Q&A**
```bash
curl -X 'POST' \
  'http://localhost:8000/qa/documents' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "document_ids": [1]
}'
```

Response:
```json
{
  "message": "Selected 1 documents for Q&A",
  "success": true
}
```

**Example 3: Ask a question**
```bash
curl -X 'POST' \
  'http://localhost:8000/qa/ask' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "What is the Central Limit Theorem?"
}'
```

Response:
```json
{
  "question": "What is the Central Limit Theorem?",
  "answer": "The Central Limit Theorem states that when you take a large enough sample from a population, the distribution of sample means will be approximately normally distributed, regardless of the original population's distribution. This is fundamental to statistical inference and allows us to make predictions about populations using sample data.\n\nSources:\n- Naked Statistics_ Stripping the Dread from the Data ( PDFDrive ).pdf (Similarity: 0.8721)",
  "processed_at": "2025-03-27T10:22:15.123456"
}
```

## Advanced Configuration

The application is highly configurable through environment variables:

- **Document Processing**: Adjust the `chunkSize` and `chunkOver` parameters to control how documents are split into chunks
- **Embedding Model**: Change the `embeddingMod` to use a different embedding model
- **LLM Model**: Modify `ollamaModel` to use a different language model

## Embedding Model and Retrieval Algorithm

### Embedding Model Choice

This application uses the `sentence-transformers/all-MiniLM-L6-v2` model for generating embeddings. Here's why:

- **Efficiency and Performance**: This model provides an excellent balance between speed and quality. It creates 384-dimensional embeddings that capture semantic meaning while being computationally efficient.

- **Versatility**: The model performs well across various text types and domains, making it suitable for diverse document collections.

- **Size and Speed**: At only 80MB, this model runs quickly even on CPU, allowing for fast document processing without requiring specialized hardware.

- **Strong Benchmarks**: It consistently scores well on semantic similarity tasks which is crucial for retrieval performance.

You can change the embedding model by updating the `embeddingMod` environment variable if you have specific requirements for your use case.

### Retrieval Algorithm

The system uses cosine similarity for retrieval, which offers several advantages:

- **Semantic Understanding**: Instead of simple keyword matching, cosine similarity with embeddings captures the semantic meaning of text, enabling more intelligent retrieval.

- **Normalization**: Cosine similarity normalizes for document length, ensuring that chunk size doesn't unduly influence retrieval results.

- **Performance**: The implementation is computationally efficient, allowing for quick retrieval from large document collections.

- **Fine-tuning Control**: The `simi_threshold` parameter (default: 0.5) lets you adjust the minimum similarity score for retrieval, while `topK` (default: 3) controls how many document chunks are retrieved for each query.

The retrieval process works as follows:

1. The user's question is converted into an embedding vector
2. This vector is compared against all document chunk embeddings using cosine similarity
3. The system retrieves the top K chunks with highest similarity scores
4. These chunks are used as context for the LLM to generate an answer
5. The response includes source information and similarity scores for transparency

## Troubleshooting

**Database connection issues**
- Ensure PostgreSQL is running and accessible
- Verify your database credentials in the .env file

**Document upload problems**
- Currently only PDF files are supported
- Check that your PDF is not corrupted or password protected

**LLM-related issues**
- Make sure Ollama is running locally or update the URL if using a remote instance
- Verify that the specified model is available in your Ollama installation

## Architecture

This application follows a clean architecture:

- **API Layer**: FastAPI routes in `api/` directory
- **Service Layer**: Business logic in `service/` directory
- **Database Layer**: Database operations in `database/` directory
- **Configuration**: Central configuration in `config.py`
