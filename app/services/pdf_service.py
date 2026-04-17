import PyPDF2

def extract_text_from_pdf(file_path: str):
    reader = PyPDF2.PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text