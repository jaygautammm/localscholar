# LocalScholar

**Offline RAG-powered research assistant for long PDF documents**

Built with LM Studio, ChromaDB, FastAPI, and React.

## Features

-  PDF upload and ingestion
-  Local LLM inference via LM Studio
-  Semantic vector search with ChromaDB
-  Multi-document support
-  Document-aware retrieval
-  Page and chapter-level citations
-  Conversational interface
-  Modern React + Tailwind UI
-  100% offline and private

## Architecture
User uploads PDF -> Text extraction + cleaning -> Hybrid recursive chunking -> Vector embeddings -> ChromaDB storage -> User asks question -> Semantic retrieval -> Context construction -> Local LLM generation -> Grounded answer with sources


## Tech Stack

**Backend:**
- FastAPI
- ChromaDB
- pypdf / PyMuPDF
- sentence-transformers
- LM Studio (OpenAI-compatible)

**Frontend:**
- React
- Vite
- Tailwind CSS
- react-markdown

## Setup

1. Install LM Studio and load a model
2. Start LM Studio local server on port 1234
3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start backend:
    ```bash
    cd backend
    uvicorn main:app --reload
    ```
5. Install frontend dependencies:
    ```bash
    cd frontend
    npm install
    ```
6. Start frontend:
    ```bash
    npm run dev
    ```
## Usage

1. Upload a PDF through the UI
2. Click "Ingest Document"
3. Ask questions about the document
4. View answers with source citations
5. Expand source cards to see full evidence
