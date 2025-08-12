import os
import tempfile
from fastapi import UploadFile
import pdfplumber
import docx2txt

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from a PDF file using pdfplumber."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(file_path: str) -> str:
    """Extracts text from a DOCX file using docx2txt."""
    return docx2txt.process(file_path).strip()

def extract_text_from_txt(file_path: str) -> str:
    """Extracts text from a TXT file."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()

async def extract_text_from_file(file: UploadFile) -> str:
    """
    Extracts text from an uploaded PDF, DOCX, or TXT file.

    Args:
        file (UploadFile): The uploaded file from FastAPI.

    Returns:
        str: Extracted plain text content.

    Raises:
        ValueError: If the file type is not supported.
    """
    ext = file.filename.lower().split(".")[-1]
    contents = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(contents)
        tmp.flush()
        tmp_path = tmp.name

    try:
        if ext == "pdf":
            return extract_text_from_pdf(tmp_path)
        elif ext in ("docx", "doc"):
            return extract_text_from_docx(tmp_path)
        elif ext == "txt":
            return extract_text_from_txt(tmp_path)
        else:
            raise ValueError("❌ Unsupported file type. Please upload a PDF, Word (.docx), or TXT document.")
    finally:
        try:
            os.remove(tmp_path)  # Clean up temp file
        except Exception:
            pass
