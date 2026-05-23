import os
import pytesseract

import config
from ppt_kb import export_slides_to_images, build_kb
from ocr_utils import ocr_image
from narrator import run_presentation
from qa_live import run_qa_voice
import shutil

def main():
    pptx = config.PPT_PATH
    out_dir = config.OUT_DIR

    slides_png_dir = os.path.join(out_dir, "slides_png")
    kb_path = os.path.join(out_dir, "slides_kb.json")

    # OCR config
    pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    print("[A] Export PPT slides to images...")
    export_slides_to_images(pptx, slides_png_dir)

    print("[B] Build KB (ppt text + notes + OCR)...")
    slides = build_kb(pptx, slides_png_dir, kb_path, ocr_image)

    print("[C] Presentation narration (Gemini -> Hume voice)...")
    #run_presentation(slides, config.OLLAMA_MODEL, config.HUME_API_KEY, out_dir)
    #run_presentation(slides, config.OLLAMA_MODEL, config.HUME_API_KEY, out_dir, config.PPT_PATH)
    run_presentation(slides, config.HUME_API_KEY, out_dir, config.PPT_PATH)

    print("[D] Live doubts mode...")
    #run_qa_voice(slides, config.OLLAMA_MODEL, config.HUME_API_KEY)
    run_qa_voice(slides, config.HUME_API_KEY)

if __name__ == "__main__":
    main()
