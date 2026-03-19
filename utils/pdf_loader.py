import fitz  # PyMuPDF library (installed via pymupdf)

def load_pdf(file_path: str):
    doc = fitz.open(file_path)  # Open the PDF file
    pages = []  # List to store extracted pages

    # Loop through each page in the PDF
    for page_number, page in enumerate(doc):
        text = page.get_text()  # Extract raw text from the page

        # Store both text and page number (metadata)
        pages.append({
            "page": page_number,
            "text": text
        })

    return pages  # Return list of pages