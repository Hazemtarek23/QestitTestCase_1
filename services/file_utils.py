import chardet
import tempfile
from fastapi import UploadFile
import pdfplumber
import docx2txt

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(file_path: str) -> str:
    return docx2txt.process(file_path).strip()

async def extract_text_from_file(file: UploadFile) -> str:
    ext = file.filename.lower().split(".")[-1]

    # Read binary content
    contents = await file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(contents)
        tmp.flush()
        tmp_path = tmp.name

    # Handle known document types
    if ext == "pdf":
        return extract_text_from_pdf(tmp_path)
    elif ext in ("docx", "doc"):
        return extract_text_from_docx(tmp_path)
    elif ext in ("txt", "csv"):
        # Detect encoding
        detected = chardet.detect(contents)
        encoding = detected.get("encoding", "utf-8")  # fallback to utf-8 if not found

        try:
            return contents.decode(encoding)
        except UnicodeDecodeError:
            raise ValueError(f"❌ Could not decode file using detected encoding: {encoding}")
    else:
        raise ValueError("❌ Unsupported file type. Please upload PDF, DOCX, or TXT.")
