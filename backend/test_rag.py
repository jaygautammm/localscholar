from rag_chain import answer_question


def main():
    questions = [
        "What does Sun Tzu say about deception?",
        "What are the five constant factors?",
        "What does Sun Tzu say about prolonged war?",
        "How should an army treat enemy soldiers?",
        "What does this book say about machine learning?"
    ]

    for question in questions:
        print("\n" + "=" * 100)
        print(f"Question: {question}")

        result = answer_question(question, n_results=5)

        print("\nAnswer:")
        print(result["answer"])

        print("\nSources:")
        for source in result["sources"]:
            print("-" * 80)
            print(f"Source {source['source_number']}")
            print(f"File: {source['file']}")
            print(f"Chapter: {source['chapter']}")
            print(f"Pages: {source['page_start']}-{source['page_end']}")
            print(f"Distance: {source['distance']}")
            print(f"Preview: {source['preview']}")


if __name__ == "__main__":
    main()