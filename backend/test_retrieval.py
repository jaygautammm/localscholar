from retriever import retrieve_chunks, build_context_from_chunks


def main():
    questions = [
        "What does Sun Tzu say about deception?",
        "What are the five constant factors?",
        "What does the book say about prolonged war?",
        "How should an army treat enemy soldiers?"
    ]

    for question in questions:
        print("\n" + "=" * 100)
        print(f"Question: {question}")

        chunks = retrieve_chunks(question, n_results=3)

        for i, chunk in enumerate(chunks, start=1):
            metadata = chunk["metadata"]

            print("\n" + "-" * 80)
            print(f"Result {i}")
            print(f"Distance: {chunk['distance']}")
            print(f"Source: {metadata.get('source')}")
            print(f"Chapter: {metadata.get('chapter')}")
            print(f"Page: {metadata.get('page_start')}")
            print("Preview:")
            print(chunk["text"][:700])

        context = build_context_from_chunks(chunks)

        print("\n" + "-" * 80)
        print("Context Preview Sent to LLM:")
        print(context[:1200])


if __name__ == "__main__":
    main()