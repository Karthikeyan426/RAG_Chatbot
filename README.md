# RAG API 🚀

A Retrieval-Augmented Generation (RAG) backend built with **FastAPI**, **PostgreSQL**, **pgvector**, **SQLModel**, **Sentence Transformers**, and **Groq's Llama 3.1 8B Instant**.

The application allows users to upload PDF documents, extract and store their contents as vector embeddings, and ask natural language questions grounded in those documents.

To improve performance and reduce LLM inference costs, the system implements a **Semantic Response Cache**. Before generating a new response, the application searches previously answered questions using vector similarity. If a highly similar question is found, the stored response is returned instantly without invoking the LLM.

---

# ✨ Features

## 👤 User Management

- User Registration
- User Login
- User Deletion

## 📄 Document Management

- Upload PDF documents
- Delete uploaded documents
- Associate documents with specific users

## 🧠 Retrieval-Augmented Generation

- PDF text extraction
- Intelligent text chunking
- Embedding generation using Sentence Transformers
- Vector similarity search using pgvector
- Context retrieval from uploaded documents
- LLM-powered answer generation using Llama 3.1 8B Instant

## ⚡ Semantic Response Cache

Before querying the LLM:

1. Generate an embedding for the incoming question.
2. Compare it against embeddings of previously answered questions.
3. If a highly similar question exists:
   - Return the cached response.
4. Otherwise:
   - Retrieve relevant document chunks.
   - Generate a new answer using the LLM.
   - Store the response for future reuse.

### Benefits

- Reduced response latency
- Lower LLM inference cost
- Reduced API usage
- Improved scalability
- Better user experience

---

# 🏗 Architecture

```text
                          ┌─────────────────────┐
                          │    Upload PDF       │
                          └──────────┬──────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │   Text Extraction   │
                          └──────────┬──────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │   Text Chunking     │
                          └──────────┬──────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │ Embedding Generation│
                          │   MiniLM-L6-v2      │
                          └──────────┬──────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │ PostgreSQL +        │
                          │ pgvector            │
                          └──────────┬──────────┘
                                     │
                                     ▼
                              User Question
                                     │
                                     ▼
                          Question Embedding
                                     │
                                     ▼
                         Semantic Cache Lookup
                                     │
                 ┌───────────────────┴───────────────────┐
                 │                                       │
                 ▼                                       ▼
        Similar Question Found                  No Similar Question
                 │                                       │
                 ▼                                       ▼
       Return Cached Response               Retrieve Relevant Chunks
                                                         │
                                                         ▼
                                              Llama 3.1 8B Instant
                                                         │
                                                         ▼
                                               Store New Response
                                                         │
                                                         ▼
                                                  Return Answer
```

---

# 🗄 Database Design

This project uses **PostgreSQL as both a relational database and a vector database**.

Instead of introducing a separate vector database, embeddings are stored directly inside PostgreSQL using the **pgvector** extension.

### Stored Data

- Users
- Documents
- Document Chunks
- Chunk Embeddings
- Chat History
- Question Embeddings
- Cached Responses

### Advantages

- Single database architecture
- Easier deployment
- Easier maintenance
- ACID-compliant storage
- Native vector similarity search
- Reduced infrastructure complexity

---

# 🛠 Tech Stack

## Backend

- FastAPI
- SQLModel
- SQLAlchemy

## Database

- PostgreSQL
- pgvector

## AI & NLP

- Sentence Transformers
- all-MiniLM-L6-v2
- Groq API
- Llama 3.1 8B Instant

## Document Processing

- PDF Text Extraction
- Text Chunking Pipeline

---

# 📦 Installation

## Clone Repository

```bash
git clone https://github.com/Karthikeyan426/RAG.git
cd RAG
```

## Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ⚙️ Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://username:password@localhost:5432/rag
GROQ_API_KEY=your_groq_api_key
```

---

# 🗄 PostgreSQL Setup

Create a PostgreSQL database and enable the pgvector extension.

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

---

# ▶️ Running the Application

```bash
uvicorn main:app --reload
```

API Documentation:

```text
http://localhost:8000/docs
```

Swagger UI will automatically provide interactive API testing.

---

# 📚 API Endpoints

## User APIs

### Register User

```http
POST /users/register
```

Request Body

```json
{
  "user_name": "karthikeyan",
  "password": "password123"
}
```

Response

```json
{
  "message": "user created"
}
```

---

### Login

```http
POST /users/login
```

Request Body

```json
{
  "user_name": "karthikeyan",
  "password": "password123"
}
```

Response

```json
{
  "message": "login success"
}
```

---

### Delete User

```http
DELETE /users/unregister/{user_name}
```

---

## Document APIs

### Upload PDF

```http
POST /docs/upload
```

Content-Type

```text
multipart/form-data
```

Form Fields

| Field | Type | Description |
|---------|---------|---------|
| user_id | string | Owner of the document |
| document | file | PDF document |

Response

```json
{
  "message": "document uploaded"
}
```

---

### Delete Document

```http
DELETE /docs/{doc_id}
```

Response

```json
{
  "message": "document deleted"
}
```

---

## Chat APIs

### Query Documents

```http
POST /users/user/chats/query
```

Request Body

```json
{
  "user_id": "user-id",
  "doc_id": "document-id",
  "question": "What is Retrieval Augmented Generation?"
}
```

Process:

1. Generate question embedding.
2. Search semantic cache.
3. If match found → return cached response.
4. Otherwise retrieve relevant document chunks.
5. Generate answer using Llama 3.1 8B Instant.
6. Store question, embedding, and response.

---

### Get Chat

```http
GET /users/user/chats/{chat_id}
```

Returns a previously stored chat.

---

### Delete Chat

```http
DELETE /users/user/chats/{chat_id}
```

Deletes a stored chat.

---

# 🧠 Embedding Model

Current embedding model:

```python
SentenceTransformer("all-MiniLM-L6-v2")
```

### Embedding Dimension

```text
384
```

The embeddings are stored directly in PostgreSQL using:

```python
Column(VECTOR(384))
```

and queried using pgvector similarity operators.

---

# ⚡ Semantic Cache Implementation

One of the key optimizations in this project is the Semantic Response Cache.

Instead of sending every question to the LLM:

1. Generate an embedding for the question.
2. Search previously answered questions using vector similarity.
3. If similarity exceeds a threshold:
   - Return stored answer.
4. Otherwise:
   - Run the full RAG pipeline.
   - Store the response for future reuse.

This significantly reduces:

- API costs
- LLM usage
- Response latency

while improving scalability.

---

# 🚀 Future Improvements

- JWT Authentication
- Password Hashing
- Conversation Memory
- Streaming Responses
- Hybrid Search (Keyword + Vector)
- Docker Support
- Kubernetes Deployment
- Alembic Database Migrations
- Multi-document Retrieval
- Source Citations
- Role-Based Access Control
- Monitoring & Analytics

---

# 📈 Learning Outcomes

This project demonstrates:

- FastAPI backend development
- REST API design
- PostgreSQL database design
- Vector databases using pgvector
- Embedding generation
- Semantic search
- Retrieval-Augmented Generation (RAG)
- LLM integration
- Query optimization through semantic caching

---

# 👨‍💻 Author

**Karthikeyan Saravanan**

 Python Developer | AI Enthusiast | Backend Developer

GitHub: https://github.com/Karthikeyan426

---

# 📄 License

This project is licensed under the MIT License.

Feel free to use, modify, and distribute it.
