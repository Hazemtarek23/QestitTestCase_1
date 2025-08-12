# utils/file_extraction.py - Simple text-only version
from fastapi import UploadFile


async def extract_text_from_file(file: UploadFile) -> str:
    """Extract text from uploaded files - simple version"""
    try:
        content = await file.read()

        # Try to decode as text
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                text = content.decode('latin1')
            except:
                text = content.decode('utf-8', errors='ignore')

        # Basic validation
        if not text.strip():
            raise Exception("File appears to be empty or contains no readable text")

        return text

    except Exception as e:
        raise Exception(f"Failed to extract text from file: {str(e)}")


# Placeholder functions for PDF and Excel generation
def text_to_pdf(text: str, output_path: str):
    """Simple text to file conversion"""
    with open(output_path.replace('.pdf', '.txt'), 'w', encoding='utf-8') as f:
        f.write(text)


def generate_test_case_excel(test_cases: list, output_path: str):
    """Simple test cases to text file"""
    with open(output_path.replace('.xlsx', '.txt'), 'w', encoding='utf-8') as f:
        f.write("TEST CASES\n" + "=" * 50 + "\n\n")
        for i, tc in enumerate(test_cases, 1):
            f.write(f"Test Case {i}:\n")
            for key, value in tc.items():
                f.write(f"{key}: {value}\n")
            f.write("\n" + "-" * 30 + "\n\n")