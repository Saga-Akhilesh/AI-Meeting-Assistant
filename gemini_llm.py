from google import genai
import config
import re

client = genai.Client(api_key=config.GEMINI_API_KEY)

def clean_text(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def make_slide_narration(slide_context: str) -> str:
    prompt = f"""
You are a professional corporate presenter.
Summarize and explain the slide content in a clear top-to-bottom order.

Rules:
- English only
- STRICT LIMIT: 45 to 70 words
- Follow slide order: title -> bullets -> any image/OCR info
- Explain meaning briefly (not just reading bullets)
- Sound conversational

SLIDE:
{slide_context}
""".strip()

    resp = client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=prompt
    )
    return clean_text(resp.text)

def answer_doubt(all_slides_context: str, question: str) -> str:
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

    resp = client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=prompt
    )
    return clean_text(resp.text)
