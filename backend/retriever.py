import chromadb

from config import CHROMA_DIR, COLLECTION_NAME


def get_collection():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def retrieve_chunks(question, n_results=5, file_name=None):
    collection = get_collection()

    query_kwargs = {
        "query_texts": [question],
        "n_results": n_results,
        "include": ["documents", "metadatas", "distances"]
    }

    # Add filter by source if file_name provided
    if file_name:
        query_kwargs["where"] = {"source": file_name}

    results = collection.query(**query_kwargs)

    retrieved = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for doc, metadata, distance in zip(documents, metadatas, distances):
        retrieved.append({
            "text": doc,
            "metadata": metadata,
            "distance": distance
        })

    return retrieved


def build_context_from_chunks(chunks):
    context_blocks = []

    for index, chunk in enumerate(chunks, start=1):
        metadata = chunk["metadata"]

        source = metadata.get("source", "Unknown Source")
        page_start = metadata.get("page_start", "Unknown Page")
        page_end = metadata.get("page_end", page_start)
        chapter = metadata.get("chapter", "Unknown Chapter")

        context_block = f"""
[Source {index}]
File: {source}
Chapter: {chapter}
Pages: {page_start}-{page_end}
Content:
{chunk["text"]}
""".strip()

        context_blocks.append(context_block)

    return "\n\n".join(context_blocks)