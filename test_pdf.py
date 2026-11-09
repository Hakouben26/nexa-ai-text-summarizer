
from pdf_reader import extract_text_from_pdf

pdf_path = input("Enter your PDF file path: ").strip().strip('"')

with open(pdf_path, "rb") as pdf_file:

    result = extract_text_from_pdf(pdf_file)

    print("\nPDF successfully read!")
    print("Pages:", result["pages"])
    print("Words:", result["words"])
    print("Characters:", result["characters"])

    print("\nExtracted text:")
    print(result["text"][:2000])
