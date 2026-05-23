# 🤖 AI Presentation Copilot

An AI-powered presentation assistant that can:

- Read PowerPoint presentations
- Extract slide content
- Generate AI narrations using LLMs
- Speak using AI voice
- Listen to audience questions
- Answer questions live through speech

---

# 🚀 Features

## 📂 PPT Processing
- Upload `.pptx` files
- Export slides as PNG images
- Extract:
  - Slide text
  - Speaker notes
  - OCR text from images

## 🧠 AI Narration
- Generate narrations using Groq LLM
- Context-aware explanations
- Smooth slide-by-slide narration

## 🔊 AI Voice
- AI speech using Hume AI TTS
- Real-time voice narration

## 🎤 Live Voice Q&A
- Voice-based audience interaction
- Speech-to-text using Vosk
- AI-generated spoken responses

## 🎞 PowerPoint Automation
- Automatic slideshow control
- Slide navigation using COM Automation

---

# 🏗 Architecture

```text
Streamlit Frontend
        ↓
PPT Upload
        ↓
PowerPoint COM Automation
        ↓
Slide Export → PNG
        ↓
OCR + PPT Text + Notes Extraction
        ↓
Knowledge Base Creation
        ↓
Groq LLM Narration
        ↓
Hume AI Voice Output
        ↓
Live Voice Q&A (Vosk STT)
```

---

# 🛠 Tech Stack

## Frontend
- Streamlit

## Backend
- Python

## AI / LLM
- Groq LLM
- Hume AI
- Vosk

## Automation
- Win32 COM Automation
- OCR (Tesseract)

---

# 📁 Project Structure

```text
AI-Presentation-Copilot/
│
├── ui_app.py
├── main.py
├── narrator.py
├── qa_live.py
├── stt_vosk.py
├── ppt_kb.py
├── groq_llm.py
├── hume_voice.py
├── ocr_utils.py
├── config.py
│
├── output/
│   ├── slides_png/
│   ├── scripts/
│   └── slides_kb.json
│
├── vosk-model/
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/AI-Presentation-Copilot.git

cd AI-Presentation-Copilot
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📦 requirements.txt

```txt
streamlit
vosk
sounddevice
keyboard
numpy
python-pptx
pytesseract
pywin32
requests
Pillow
```

---

# 🔑 API Setup

## Groq API

https://console.groq.com/

## Hume AI

https://platform.hume.ai/

---

# 🧠 Download Vosk Model

Download from:

https://alphacephei.com/vosk/models

Recommended model:

```text
vosk-model-en-in-0.5
```

Rename folder to:

```text
vosk-model
```

Place it in project root.

---

# 📝 Configure `config.py`

```python
GROQ_API_KEY = "your_groq_key"
HUME_API_KEY = "your_hume_key"

OUT_DIR = "output"

SAMPLE_RATE = 16000
CHANNELS = 1
BLOCK_SIZE = 8000

MIC_DEVICE_INDEX = 19
```

---

# ▶️ Run Application

```bash
streamlit run ui_app.py
```

---

# 🎤 Voice Controls

## Start Listening

Press:

```text
CTRL
```

## Stop Listening

Press:

```text
CTRL again
```

---

# 🔥 Future Enhancements

- Live slide preview
- AI avatar presenter
- GPT-4 / Gemini support
- Multi-language narration
- Real-time captions
- Cloud deployment
