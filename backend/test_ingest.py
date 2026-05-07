from pathlib import Path

from ingest import ingest_pdf


def main():
    pdf_path = Path("../documents/AOW.pdf")

    if not pdf_path.exists():
        print("PDF not found. Put sample_book.pdf inside the documents folder.")
        return

    result = ingest_pdf(
        pdf_path=pdf_path,
        reset_collection=True,
        max_chars=1200,
        overlap_chars=150
    )

    print(result)


if __name__ == "__main__":
    main()