# pdf_to_text.py
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path):
    pdf_text = ""

    # Read the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            pdf_text += page.extract_text() + "\n"  # Extract and add each page's text

    return pdf_text


def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(text)
