import requests
import re
import config

def clean_text(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def ollama_generate(model: str, prompt: str) -> str:
    url = "http://localhost:11434/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}
    r = requests.post(url, json=payload, timeout=180)
    r.raise_for_status()
    return clean_text(r.json().get("response", ""))

def make_slide_narration(model: str, slide_context: str) -> str:
    prompt = f"""
You are a corporate presenter.
Create a professional narration for the slide below.

Rules:
- Formal corporate English
- STRICT LIMIT: {config.NARRATION_WORD_MIN} to {config.NARRATION_WORD_MAX} words maximum
- No fluff, no filler
- Do not mention OCR
- Do not hallucinate; use only slide content
- Start directly (no long welcome each slide)

SLIDE:
{slide_context}
""".strip()
    return ollama_generate(model, prompt)

def answer_doubt(model: str, all_slides_context: str, question: str) -> str:
    prompt = f"""
You are Akhilesh's AI assistant.
Answer the question using ONLY the slides content.

Rules:
- English only
- 2 to 3 lines maximum
- If not present in slides, say:
  "This is not covered in the shared slides. I'll confirm and get back to you."

SLIDES:
{all_slides_context}

QUESTION:
{question}
""".strip()
    return ollama_generate(model, prompt)

