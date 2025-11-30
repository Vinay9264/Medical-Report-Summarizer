import easyocr
from PIL import Image

reader = easyocr.Reader(["en"], gpu=False)


def extract_text_from_image(image_path: str)->str:
    try:
        result = reader.readtext(image_path, detail=0)
        return "\n".join(result)
    except Exception as e:
        return f"OCR Error (image): {str(e)}"
