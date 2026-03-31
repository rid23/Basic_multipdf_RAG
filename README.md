# Multi-PDF RAG (Retrieval Augmented Generation) System

![RAG Banner](https://img.shields.io/badge/RAG-Multi--PDF-blue) ![Python](https://img.shields.io/badge/Python-3.11+-green) ![LangChain](https://img.shields.io/badge/LangChain-1.2.10-orange)

A powerful Multi-PDF Retrieval Augmented Generation system that enables semantic search and querying across multiple PDF documents. This project processes PDF files, converts them into embeddings, stores them in a vector database, and allows users to query the knowledge base using natural language.

---

## Overview

This RAG system performs the following operations:

1. **PDF Loading** - Loads multiple PDF documents from a specified directory
2. **Text Processing** - Splits large documents into manageable chunks
3. **Embedding Generation** - Converts text chunks into vector embeddings using transformer models
4. **Vector Storage** - Stores embeddings in ChromaDB for efficient similarity search
5. **Semantic Querying** - Retrieves relevant document sections based on user queries

---

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   PDFs      │────▶│  Loader     │────▶│  Splitter   │────▶│ Embedding   │
│  (Source)   │     │ (PyMuPDF)   │     │ (Recursive) │     │ (SBERT)     │
└─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘
                                                                    │
                                                                    ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   User      │────▶│   Query     │────▶│  ChromaDB   │◀────│  Vector     │
│  (Query)    │     │  (Search)   │     │  (Store)    │     │  (Embeddings)│
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

---

## Tech Stack

| Technology | Purpose | Logo |
|-------------|---------|------|
| **Python** | Programming Language | <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width="40"/> |
| **LangChain** | LLM Framework & Text Splitting | <img src="https://python.langchain.com/img/logo-dark-wordmark.svg" width="80"/> |
| **ChromaDB** | Vector Database | <img src="https://www.trychroma.com/logo.svg" width="40"/> |
| **Sentence Transformers** | Embedding Generation | <img src="https://sbert.net/images/logo.png" width="60"/> |
| **PyMuPDF** | PDF Parsing | <img src="https://pymupdf.readthedocs.io/en/latest/_static/HiRes.png" width="40"/> |
| **scikit-learn** | Cosine Similarity | <img src="https://scikit-learn.org/stable/_static/scikit-learn-logo-small.png" width="60"/> |
| **Rich** | Terminal Formatting | <img src="https://github.com/Textualize/rich/raw/master/imgs/logo.svg" width="40"/> |
| **NumPy** | Numerical Computing | <img src="https://upload.wikimedia.org/wikipedia/commons/3/31/NumPy_logo_2020.svg" width="60"/> |
| **Google Gemini 2.5 Flash** | LLM for Answer Generation | <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" width="40"/> |

---

## Project Structure

```
langchain_rag/
├── rag_main.py              # Main script - PDF loading, embedding, vector storage
├── rag_query.py             # Query client for semantic search
├── llm_brain.py             # LLM brain using Google Gemini 2.5 Flash for answer generation
├── chroma_db_inspector.py   # Utility to inspect vector store contents
├── pdfs/                    # Directory containing PDF files
├── vector_store/            # Persistent ChromaDB storage
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## Scripts

### 1. `rag_main.py` - Main RAG Pipeline

**Purpose:** Core functionality for loading PDFs, generating embeddings, and populating the vector store.

**Key Functions:**
- `load_pdf(file_path)` - Loads all PDF files from a directory using PyMuPDFLoader
- `text_splitter(documents, chunk_size, chunk_overlap)` - Splits documents into overlapping chunks
- `EmbeddingManager` class - Manages SentenceTransformer embedding model
- `VectorStore` class - Handles ChromaDB operations (add, delete, list collections)
- `intialize_vector_store_add_documents()` - Main pipeline function

**Usage:**
```bash
python rag_main.py
# Enter 'add' to add documents to vector store
# Enter 'query' to query existing documents
```

---

### 2. `rag_query.py` - Query Client

**Purpose:** Enables semantic search across the vector store using natural language queries.

**Key Class:**
- `query_client` - Class for querying ChromaDB collection
  - `query_collection(query, n_results)` - Returns top-k relevant document chunks

**Usage:**
```bash
python rag_query.py
# Enter your query when prompted
```

Or import in other scripts:
```python
from rag_query import query_client
client = query_client()
client.query_collection("your question", n_results=5)
```

---

### 3. `chroma_db_inspector.py` - Vector Store Inspector

**Purpose:** Debugging and inspection utility to view vector store contents.

**Features:**
- Lists all collections in the vector store
- Shows document count, metadata, and sample embeddings
- Useful for troubleshooting and data verification

**Usage:**
```bash
python chroma_db_inspector.py
```

---

### 4. `llm_brain.py` - LLM Brain (Google Gemini 2.5 Flash)

**Purpose:** Provides the AI "brain" for the RAG system. Uses Google Gemini 2.5 Flash model to generate natural language answers based on retrieved context from the vector store.

**Key Function:**
- `the_brain(llm, context, query)` - Generates answers using a RAG chain
  - Takes an LLM instance, retrieved context, and user query
  - Uses LangChain's PromptTemplate and StrOutputParser
  - Returns a concise, context-aware answer

**Integration with RAG Pipeline:**
```python
from llm_brain import the_brain
from rag_query import query_client
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Query vector store
query_client_instance = query_client()
context_docs = query_client_instance.query_collection("your question", n_results=5)

# Format context
context = "\n\n".join([doc[0] for doc in context_docs])

# Generate answer
answer = the_brain(llm, context, "your question")
print(answer)
```

**Usage:**
```bash
# Import and use in your own scripts
python -c "
from llm_brain import the_brain
from rag_query import query_client
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
client = query_client()
docs = client.query_collection('What is SQL injection?', n_results=3)
context = '\n\n'.join([d[0] for d in docs])
print(the_brain(llm, context, 'What is SQL injection?'))
"
```

---

## Installation

1. **Create and activate virtual environment:**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Add PDFs:**
Place your PDF files in the `pdfs/` directory.

---

## Quick Start

### Step 1: Add Documents to Vector Store
```bash
python rag_main.py
# Select 'add' when prompted
```

### Step 2: Query Your Documents
```bash
python rag_main.py
# Select 'query' when prompted
# Enter your question
```

---

## Key Libraries Used

| Library | Version | Purpose |
|---------|---------|---------|
| `langchain-community` | 0.4.1 | Document loaders (PyPDFLoader, PyMuPDFLoader) |
| `langchain-text-splitters` | 1.1.0 | Recursive text splitting |
| `chromadb` | 1.5.1 | Vector database for embeddings |
| `sentence-transformers` | 5.2.3 | Generate text embeddings (all-MiniLM-L6-v2) |
| `pymupdf` | 1.27.1 | High-performance PDF parsing |
| `numpy` | 2.4.2 | Numerical operations |
| `scikit-learn` | 1.8.0 | Cosine similarity calculations |
| `rich` | 14.3.2 | Terminal output formatting |

---

## Configuration

### Embedding Model
Default: `all-MiniLM-L6-v2` (fast, lightweight, 384 dimensions)

To change the model, modify `rag_main.py`:
```python
embedding_manager = EmbeddingManager(model_name='your-model-name')
```

### Chunk Size
Default: 1000 characters with 200 character overlap

```python
all_documents_chunks = text_splitter(all_documents, chunk_size=1500, chunk_overlap=300)
```

### Collection Name
Default: `hacking_pdfs`

```python
vector_store = VectorStore(collection_name="your_collection_name")
```

### LLM Model (llm_brain.py)
Default: `gemini-2.0-flash` (Google Gemini 2.5 Flash)

To use with the LLM brain:
```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
```

Set your Google API key:
```bash
export GOOGLE_API_KEY="your-api-key"
# Windows
set GOOGLE_API_KEY=your-api-key
```

---

## To Improve

### 🔴 High Priority

1. ~~Add LLM Integration for Answer Generation~~
   - ~~Currently returns raw document chunks~~
   - ~~Integrate with OpenAI, Anthropic, or local LLMs (Llama3, Mistral)~~
   - ~~Use LangChain's `RetrievalQA` chain for complete RAG pipeline~~
   - ✅ **COMPLETED** - Added `llm_brain.py` with Google Gemini 2.5 Flash integration

2. Implement Hybrid Search
   - Combine dense (semantic) embeddings with sparse (BM25) search
   - Use `langchain-community`'s `EnsembleRetriever`

3. **Add Document Metadata Filtering**
   - Enable filtering by date, source file, author, etc.
   - Implement metadata-based pre-filtering before embedding search

4. **Improve PDF OCR Support**
   - Add support for scanned/image-based PDFs
   - Integrate Tesseract or AWS Textract

### 🟡 Medium Priority

5. **Add Incremental Document Updates**
   - Implement document versioning
   - Support updating/deleting specific documents
   - Add change detection (hash-based)

6. **Implement Caching**
   - Cache embeddings for unchanged documents
   - Use Redis or disk-based cache

7. **Add Support for Other Document Types**
   - DOCX, TXT, HTML, Markdown
   - Use LangChain's universal document loaders

8. **Improve Error Handling & Logging**
   - Add structured logging (loguru)
   - Implement retry mechanisms
   - Add error recovery

9. **Add Rate Limiting & Batching**
   - Batch embedding generation for large document sets
   - Add progress bars and checkpoints

### 🟢 Low Priority

10. **Add Web Interface**
    - Streamlit or Gradio UI
    - File upload, chat interface

11. **Multi-language Support**
    - Use multilingual embedding models
    - Add language detection

12. **API Server**
    - FastAPI/Flask REST API
    - Authentication, rate limiting

13. **Performance Monitoring**
    - Query latency tracking
    - Embedding generation time metrics

14. **Use Advanced Vector Stores**
    - Pinecone, Weaviate, Milvus for production
    - Add replication and sharding

15. **Test Coverage**
    - Unit tests for each component
    - Integration tests for pipeline

---

## Pending Updates (llm_brain.py)

The following items need to be completed for full LLM integration:

1. **Add Google Gemini to requirements.txt**
   - Missing: `langchain-google-genai` package
   - Add: `google-generativeai` package

2. **Create unified main script**
   - Integrate `llm_brain.py` with `rag_main.py` and `rag_query.py`
   - Provide end-to-end RAG pipeline with answer generation

3. **Environment Variables**
   - Add `GOOGLE_API_KEY` configuration for Gemini authentication

4. **Extend llm_brain.py**
   - Add error handling for API failures
   - Add support for streaming responses
   - Add configurable prompt templates

---

## Example Output

```
loading pdfs from D:\langchain_rag\pdfs
Loaded 15 documents from sample.pdf
Total documents loaded: 15
Loading embedding model: all-MiniLM-L6-v2
Embedding model "all-MiniLM-L6-v2" loaded successfully.
Generate Embeddings for 48 texts
Generated embeddings with shape : (48, 384)
Vector store initialized : Collection -> hacking_pdfs
adding 48
Vector Store Populataion complete.

Query : What is SQL injection?
Number of results: 5
Number of unique results: 3
Result 1:
Document: SQL injection is a code injection technique...
Source: hacking_guide.pdf
--------------------
```

---



---

## Author

Riddhi Bhattacharya
