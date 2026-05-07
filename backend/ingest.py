from pathlib import Path
import chromadb

from config import CHROMA_DIR, COLLECTION_NAME
from pdf_loader import extract_pdf_pages
from chunkers import hybrid_recursive_chunk_page, estimate_chapter


def get_chroma_collection(reset=False):
    """
    Create or load a persistent ChromaDB collection.
    """
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    if reset:
        try:
            client.delete_collection(name=COLLECTION_NAME)
            print(f"Deleted existing collection: {COLLECTION_NAME}")
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "LocalScholar PDF book knowledge base"}
    )

    return collection


def build_chunks_from_pdf(pdf_path, max_chars=1200, overlap_chars=150):
    """
    Converts a PDF into chunk records with metadata.
    """
    pdf_path = Path(pdf_path)
    pages = extract_pdf_pages(pdf_path)

    all_records = []
    current_chapter = "Unknown Chapter"

    for page in pages:
        page_number = page["page_number"]
        page_text = page["text"]

        detected_chapter = estimate_chapter(page_text)

        if detected_chapter != "Unknown Chapter":
            current_chapter = detected_chapter

        chunks = hybrid_recursive_chunk_page(
            page_text,
            max_chars=max_chars,
            overlap_chars=overlap_chars
        )

        for chunk_index, chunk_text in enumerate(chunks):
            chunk_id = f"{pdf_path.stem}_p{page_number}_c{chunk_index}"

            record = {
                "id": chunk_id,
                "text": chunk_text,
                "metadata": {
                    "source": pdf_path.name,
                    "page_start": page_number,
                    "page_end": page_number,
                    "chapter": current_chapter,
                    "chunk_index": chunk_index,
                    "chunking_strategy": "hybrid_recursive",
                    "char_count": len(chunk_text),
                    "word_count": len(chunk_text.split())
                }
            }

            all_records.append(record)

    return all_records


def ingest_pdf(pdf_path, reset_collection=False, max_chars=1200, overlap_chars=150):
    """
    Ingest one PDF into ChromaDB.
    """
    collection = get_chroma_collection(reset=reset_collection)

    records = build_chunks_from_pdf(
        pdf_path=pdf_path,
        max_chars=max_chars,
        overlap_chars=overlap_chars
    )

    if not records:
        print("No chunks created. Nothing to ingest.")
        return {
            "source": str(pdf_path),
            "chunks_indexed": 0
        }

    ids = [record["id"] for record in records]
    documents = [record["text"] for record in records]
    metadatas = [record["metadata"] for record in records]

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(f"Indexed {len(records)} chunks from {Path(pdf_path).name}")

    return {
        "source": str(pdf_path),
        "chunks_indexed": len(records)
    }