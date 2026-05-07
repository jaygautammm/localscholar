from pathlib import Path
import shutil
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import DOCUMENTS_DIR, CHROMA_DIR, COLLECTION_NAME
from ingest import ingest_pdf, get_chroma_collection
from rag_chain import answer_question


app = FastAPI(
    title="LocalScholar API",
    description="Offline RAG-powered research assistant for long PDFs",
    version="2.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    n_results: int = 5
    file_name: Optional[str] = None


class IngestRequest(BaseModel):
    file_name: str
    reset_collection: bool = False
    max_chars: int = 1200
    overlap_chars: int = 150


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "LocalScholar backend is running"
    }


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

    save_path = DOCUMENTS_DIR / file.filename

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = save_path.stat().st_size

    return {
        "message": "PDF uploaded successfully",
        "file_name": file.filename,
        "size_bytes": file_size,
        "saved_to": str(save_path)
    }


@app.post("/ingest")
def ingest_document(request: IngestRequest):
    pdf_path = DOCUMENTS_DIR / request.file_name

    if not pdf_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"File not found: {request.file_name}"
        )

    result = ingest_pdf(
        pdf_path=pdf_path,
        reset_collection=request.reset_collection,
        max_chars=request.max_chars,
        overlap_chars=request.overlap_chars
    )

    return {
        "message": "Ingestion completed",
        "result": result
    }


@app.post("/chat")
def chat(request: ChatRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        result = answer_question(
            question=question,
            n_results=request.n_results,
            file_name=request.file_name
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


@app.get("/documents")
def list_documents():
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

    pdf_files = []

    for file_path in DOCUMENTS_DIR.iterdir():
        if file_path.is_file() and file_path.suffix.lower() == ".pdf":
            pdf_files.append({
                "file_name": file_path.name,
                "size_bytes": file_path.stat().st_size
            })

    return {
        "documents": pdf_files,
        "count": len(pdf_files)
    }


@app.delete("/reset")
def reset_collection():
    try:
        collection = get_chroma_collection(reset=True)
        return {
            "message": f"Collection '{COLLECTION_NAME}' reset successfully."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))