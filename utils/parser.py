import fitz  # PyMuPDF

def extract_text_from_pdf(file) -> str:
    """
    Extracts text from a PDF file using PyMuPDF.
    :param file: Uploaded PDF file
    :return: Extracted plain text
    """
    text = ""
    try:
        # Load PDF using PyMuPDF
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
    except Exception as e:
        text = f"Error reading PDF: {e}"
    return text
