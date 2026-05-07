import re


def estimate_chapter(text):
    """
    Detect chapter/section headings.

    Supports:
    - Chapter 1
    - CHAPTER I
    - I. LAYING PLANS
    - II. WAGING WAR
    """
    patterns = [
        r"(Chapter\s+\d+[:\-\s]?.*)",
        r"(CHAPTER\s+\d+[:\-\s]?.*)",
        r"(Chapter\s+[IVXLCDM]+[:\-\s]?.*)",
        r"(CHAPTER\s+[IVXLCDM]+[:\-\s]?.*)",
        r"(^|\n)([IVXLCDM]+\.\s+[A-Z][A-Z\s\-,';:]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            return match.group(match.lastindex).strip()

    return "Unknown Chapter"


def split_by_paragraphs(text):
    paragraphs = re.split(r"\n\s*\n", text)

    cleaned = []
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if paragraph:
            cleaned.append(paragraph)

    return cleaned


def split_by_sentences(text):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


def merge_units(units, max_chars=1200, overlap_chars=150):
    chunks = []
    current = ""

    for unit in units:
        if len(current) + len(unit) + 1 <= max_chars:
            current += "\n" + unit if current else unit
        else:
            if current:
                chunks.append(current.strip())

            if overlap_chars > 0 and current:
                overlap = current[-overlap_chars:]
                current = overlap + "\n" + unit
            else:
                current = unit

    if current.strip():
        chunks.append(current.strip())

    return chunks


def hybrid_recursive_chunk_page(page_text, max_chars=1200, overlap_chars=150):
    """
    Hybrid recursive chunking for one page.

    Strategy:
    1. Split by paragraphs.
    2. If paragraph is too large, split by sentences.
    3. If sentence is too large, split by characters.
    """
    paragraphs = split_by_paragraphs(page_text)

    final_units = []

    for paragraph in paragraphs:
        if len(paragraph) <= max_chars:
            final_units.append(paragraph)
        else:
            sentences = split_by_sentences(paragraph)

            for sentence in sentences:
                if len(sentence) <= max_chars:
                    final_units.append(sentence)
                else:
                    for i in range(0, len(sentence), max_chars):
                        final_units.append(sentence[i:i + max_chars])

    chunks = merge_units(
        final_units,
        max_chars=max_chars,
        overlap_chars=overlap_chars
    )

    return chunks