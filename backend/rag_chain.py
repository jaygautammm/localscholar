from retriever import retrieve_chunks, build_context_from_chunks
from llm import ask_local_llm


def answer_question(question, n_results=5, file_name=None):
    """
    Full RAG pipeline with optional document filtering
    """
    chunks = retrieve_chunks(
        question=question,
        n_results=n_results,
        file_name=file_name
    )

    if not chunks:
        return {
            "question": question,
            "answer": "No relevant information found in the indexed documents.",
            "sources": []
        }

    context = build_context_from_chunks(chunks)

    answer = ask_local_llm(
        question=question,
        context=context
    )

    sources = []

    for index, chunk in enumerate(chunks, start=1):
        metadata = chunk["metadata"]

        sources.append({
            "source_number": index,
            "file": metadata.get("source"),
            "chapter": metadata.get("chapter"),
            "page_start": metadata.get("page_start"),
            "page_end": metadata.get("page_end"),
            "distance": chunk.get("distance"),
            "preview": chunk["text"][:300],
            "full_text": chunk["text"]
        })

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }