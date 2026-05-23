from PIL import Image
import pytesseract
import re

def clean_text(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def ocr_image(image_path: str) -> str:
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return clean_text(text)
