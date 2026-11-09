
from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    """Extract readable text from an uploaded PDF."""

    if uploaded_file is None:
        raise ValueError("Please upload a PDF file.")

    try:
        reader = PdfReader(uploaded_file)

        if reader.is_encrypted:
            raise ValueError("This PDF is password-protected.")

        total_pages = len(reader.pages)

        if total_pages == 0:
            raise ValueError("This PDF contains no pages.")

        extracted_pages = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text and page_text.strip():
                extracted_pages.append(page_text.strip())

        full_text = "\n\n".join(extracted_pages)

        if not full_text.strip():
            raise ValueError(
                "No readable text found in this PDF. "
                "It may be a scanned document."
            )

        return {
            "text": full_text,
            "pages": total_pages,
            "words": len(full_text.split()),
            "characters": len(full_text)
        }

    except ValueError:
        raise

    except Exception as error:
        raise RuntimeError(
            f"PDF extraction failed: {error}"
        ) from error
