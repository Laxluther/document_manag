# Document Management & RAG-based Q&A API

Hello, and welcome to our Document Management and RAG-based Question & Answering application! This application assists you in document management and retrieving smart answers from your document repository.

## Features

- **Document Upload**: Simple upload of PDF documents into the system
- **Smart Document Processing**: Your documents are processed into chunks automatically and indexed for retrieval efficiency
- **Powerful Q&A**: Pose questions in natural language and receive answers on the basis of your uploaded documents
- **Document Selection**: Select which documents to use in the knowledge base for answering questions

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

3. **Set environment variables**

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

4. **Run the application**

```bash
uvicorn main:app --reload
```

Your API will be available at http://localhost:8000. Access http://localhost:8000/docs for the Swagger UI documentation.

## How to Use the API

### 1. Upload Documents

Upload your PDF files to make them available for querying.

```bash
curl -X 'POST' \
  'http://localhost:8000/documents/upload'
```
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
'http://localhost:8000/qa/documents'
 -H 'accept: application/json'
 -H 'Content-Type: application/json'
 -d '{  
 "document_ids": [1, 2]  
}'
```

### 4. Ask Questions

You can now ask questions regarding your documents!

```bash
curl -X 'POST' 
  'http://localhost:8000/qa/ask' 
  -H 'accept: application/json' 
  -H 'Content-Type: application/json' 
  -d '{  
  "question": "What are the key concepts in chapter 3?"  
}'
```

## Examples

**Example 1: Upload a document**
```bash
curl -X 'POST' "\"}]
`'http://localhost:8000/documents/upload' `
-H 'accept: application/json'
-H 'Content-Type: multipart/form-data'
-F 'file=@statistics_textbook.pdf'

Response:
```json
{
  "message": "PDF document uploaded and processed successfully with ID: 1",
  "success": true
}
```

**Example 2: Select documents for Q&A**
```bash
curl -X 'POST'
  'http://localhost:8000/qa/documents'
  -H 'accept: application/json'
  -H 'Content-Type: application/json'
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
  "question": "What is the Central Limit Theorem?"
```
"answer": "The Central Limit Theorem tells us that if you take a sufficiently large sample from a population, the distribution of sample means will be nearly normally distributed, no matter what the original population's distribution is. This is the basis for statistical inference and enables us to make inferences about populations based on sample data.

Sources:
- Naked Statistics_ Stripping the Dread from the Data ( PDFDrive ).pdf (Similarity: 0.8721)",
  "processed_at": "2025-03-27T10:22:15.123456"
```

## Advanced Configuration

The application is extremely configurable using environment variables:

- **Document Processing**: Modify the `chunkSize` and `chunkOver` parameters to decide how documents are divided into chunks
- **Embedding Model**: Modify the `embeddingMod` to employ a different embedding model
- **LLM Model**: Modify `ollamaModel` to employ a different language model

## Embedding Model and Retrieval Algorithm

### Embedding Model Choice

This application employs the `sentence-transformers/all-MiniLM-L6-v2` model for producing embeddings. Here's why:

- **Efficiency and Performance**: The model achieves a great balance between speed and quality. It produces 384-dimensional embeddings that are semantically meaningful and computationally efficient.

- **Versatility**: The model is good at handling different types of text and domains and can be applied to different collections of documents.

- **Size and Speed**: This model weighs only 80MB and can run fast even on CPU, enabling fast document processing without needing special hardware.

- **Robust Benchmarks**: It performs well on semantic similarity tasks consistently, which is very important for retrieval performance.

You can modify the embedding model by setting the `embeddingMod` environment variable if you have particular needs for your application.

### Retrieval Algorithm

The system relies on cosine similarity for retrieval, which has several benefits:

- **Semantic Understanding**: Rather than keyword matching, cosine similarity with embeddings understands the semantic content of text, making retrieval more intelligent.

- **Normalization**: Cosine similarity normalizes document length, so chunk size does not unfairly skew retrieval outcomes.

- **Performance**: The implementation is efficient computationally, so retrieval is fast from large collections of documents.

- **Tuning Control**: The `simi_threshold` parameter (default: 0.5) allows you to set the minimum similarity score for retrieval, and `topK` (default: 3) determines the number of document chunks to retrieve per query.

The retrieval process is as follows:

1. The user's question is embedded into a vector
2. This vector is matched with all document chunk embeddings based on cosine similarity
3. The system returns top K chunks with highest similarity scores
4. Chunks are utilized as context for the LLM to produce a response
5. The answer contains source information and similarity scores for transparency

## Troubleshooting

**Database connection issues**
- Make sure PostgreSQL is running and accessible
- Double-check your database credentials in the.env file

**Document upload issues**
- Only PDF files are supported at the moment
- Make sure your PDF is not corrupted or password-protected

**LLM-related issues**
- Ensure Ollama is running locally or update the URL if a remote instance is being used
- Ensure that the model mentioned is present in your Ollama installation

## Architecture

The application is organized with clean architecture:

- **API Layer**: FastAPI routes in `api/` directory
- **Service Layer**: Business logic in `service/` directory
- **Database Layer**: Database operations in `database/` directory
- **Configuration**: Central configuration in `config.py`

## Contributing

Feel free to make any contributions. A Pull Request would be most appreciated.

## License

Project licensed under the MIT License - see the LICENSE file for details.
