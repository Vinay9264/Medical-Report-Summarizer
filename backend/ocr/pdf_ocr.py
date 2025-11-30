import easyocr
from pdf2image import convert_from_path
import os

reader = easyocr.Reader(["en"], gpu=False)

#PDF -> images -> text

def extract_text_from_pdf(pdf_path: str)->str:
    try:
        pages = convert_from_path(pdf_path)

        text_results = []

        for i, page in enumerate(pages):
            temp_img = f"temp_page_{i}.jpg"
            page.save(temp_img, "JPEG")

            extracted = reader.readtext(temp_img, detail=0)
            text_results.append("\n".join(extracted))

            os.remove(temp_img)

        return "\n\n".join(text_results)

    except Exception as e:
        return f"OCR Error (pdf): {str(e)}"
