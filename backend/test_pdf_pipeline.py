from pathlib import Path

from pdf_loader import extract_pdf_pages
from chunkers import hybrid_recursive_chunk_page, estimate_chapter


def main():
    pdf_path = Path("../documents/AOW.pdf")

    if not pdf_path.exists():
        print("Put a PDF named sample_book.pdf inside the documents folder.")
        return

    pages = extract_pdf_pages(pdf_path)

    print(f"Extracted {len(pages)} pages.")

    total_chunks = 0

    for page in pages[:5]:
        page_number = page["page_number"]
        text = page["text"]

        chapter = estimate_chapter(text)
        chunks = hybrid_recursive_chunk_page(text)

        print("\n" + "=" * 80)
        print(f"Page: {page_number}")
        print(f"Chapter guess: {chapter}")
        print(f"Chunks created: {len(chunks)}")

        for index, chunk in enumerate(chunks[:2]):
            print("-" * 40)
            print(f"Chunk {index + 1}")
            print(chunk[:500])

        total_chunks += len(chunks)

    print("\nPipeline test complete.")
    print(f"Chunks from first 5 pages: {total_chunks}")


if __name__ == "__main__":
    main()