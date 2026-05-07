from pypdf import PdfReader
import re

def extract_pdf_pages(pdf_path):
    """
    Extract text from a PDF page by page.

    Returns:
        [
            {
                "page_number": 1,
                "text": "..."
            },
            ...
        ]
    """
    reader = PdfReader(pdf_path)
    pages = []

    for index, page in enumerate(reader.pages):
        text = page.extract_text() or ""

        cleaned_text = clean_text(text)

        if cleaned_text.strip():
            pages.append({
                "page_number": index + 1,
                "text": cleaned_text
            })

    return pages


def clean_text(text):
    """
    Clean PDF text while fixing broken line structure.

    Handles:
    - extra spaces between words
    - one-word-per-line extraction
    - page numbers
    - basic heading preservation
    """
    text = text.replace("\x00", " ")
    text = text.replace("\r", "\n")

    raw_lines = text.split("\n")

    lines = []

    for line in raw_lines:
        # Collapse multiple spaces inside each line
        line = re.sub(r"\s+", " ", line).strip()

        if not line:
            continue

        # Remove simple page numbers
        if line.isdigit() and len(line) <= 4:
            continue

        lines.append(line)

    blocks = []
    current_paragraph = ""

    for line in lines:
        if is_probable_heading(line):
            if current_paragraph:
                blocks.append(current_paragraph.strip())
                current_paragraph = ""

            blocks.append(line.strip())
            continue

        if current_paragraph:
            current_paragraph += " " + line
        else:
            current_paragraph = line

        # If line ends with sentence-ending punctuation, close paragraph.
        if line.endswith((".", "!", "?", ".”", "’")):
            blocks.append(current_paragraph.strip())
            current_paragraph = ""

    if current_paragraph:
        blocks.append(current_paragraph.strip())

    return "\n\n".join(blocks)


def is_probable_heading(line):
    """
    Detect simple book headings while avoiding false positives like the pronoun 'I'.
    """
    stripped = line.strip()

    if not stripped:
        return False

    # Never treat a single character as a heading
    if len(stripped) == 1:
        return False

    # Avoid treating standalone Roman numerals as headings unless they have a dot/title
    if re.fullmatch(r"[IVXLCDM]+", stripped):
        return False

    # Avoid very long lines
    if len(stripped) > 90:
        return False

    # Chapter headings:
    # CHAPTER I, Chapter 1, etc.
    if re.match(r"^(Chapter|CHAPTER)\s+([0-9]+|[IVXLCDM]+)", stripped):
        return True

    # Roman numeral section headings:
    # I. LAYING PLANS
    # II. WAGING WAR
    if re.match(r"^[IVXLCDM]+\.\s+[A-Z][A-Z\s\-,';:]+$", stripped):
        return True

    # Short all-caps headings, but require at least 2 words
    # Example: THE ART OF WAR
    words = stripped.split()
    if stripped.isupper() and len(words) >= 2 and len(words) <= 8:
        return True

    return False