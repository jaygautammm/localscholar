from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS_DIR = BASE_DIR / "documents"
CHROMA_DIR = BASE_DIR / "chroma_db"
PROCESSED_DIR = BASE_DIR / "processed"

COLLECTION_NAME = "book_knowledge_base"

LM_STUDIO_BASE_URL = "http://localhost:1234/v1"
LM_STUDIO_API_KEY = "lm-studio"
LM_STUDIO_MODEL = "dolphin-2.8-mistral-7b-v02"