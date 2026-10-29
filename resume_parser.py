
import re
import pymupdf # PyMuPDF


def extract_resume_text(pdf_path):
    """Extract text from a text-based PDF resume."""

    text = ""

    with pymupdf.open(pdf_path) as document:
        for page in document:
            text += page.get_text() + "\n"

    if not text.strip():
        raise ValueError(
            "No text found. This may be a scanned PDF."
        )

    return text


def clean_text(text):
    """Normalize text before comparing documents."""

    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)

    return text.strip()
