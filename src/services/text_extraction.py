import io
import csv
from pypdf import PdfReader  

def extract_text_from_pdf(binary_content):
    """
    Extract text from a PDF binary content.
    """
    reader = PdfReader(io.BytesIO(binary_content))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or "" 
    return text

def extract_text_from_csv(binary_content):
    """
    Extract text from a CSV binary content.
    """
    text = ""
    csv_file = io.StringIO(binary_content.decode("utf-8"))
    reader = csv.reader(csv_file)
    for row in reader:
        text += " ".join(row) + "\n"
    return text

def extract_text(file_type: str, binary_content):
    """
    Extract text based on the file type (PDF or CSV).
    """
    if file_type.lower() == "pdf":
        return extract_text_from_pdf(binary_content)
    elif file_type.lower() == "csv":
        return extract_text_from_csv(binary_content)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
