import os
import json
import base64
import subprocess
from pathlib import Path
import tempfile
import winsound
import requests
import config


def _ffmpeg_exists(path: str) -> bool:
    return os.path.exists(path)


def webm_to_wav(webm_path: str, wav_path: str, ffmpeg_path: str):
    cmd = [
    ffmpeg_path, "-y",
    "-i", webm_path,
    "-af", "highpass=f=80, lowpass=f=8000, afftdn",  # ✅ noise reduction
    "-ar", "16000",
    "-ac", "1",
    "-f", "wav",
    wav_path
    ]

    subprocess.run(cmd, check=True, capture_output=True)


def hume_tts_stream_webm(api_key: str, text: str, voice_id: str) -> bytes:
    """
    Hume TTS Streaming JSON endpoint:
    POST https://api.hume.ai/v0/tts/stream/json
    Header: X-Hume-Api-Key
    Body: version + utterances[{text, voice{id}}]

    Returns: WEBM/opus bytes (base64 decoded from streaming JSON).
    """
    url = "https://api.hume.ai/v0/tts/stream/json"

    headers = {
        "X-Hume-Api-Key": api_key,
        "Accept": "application/json; charset=utf-8",
        "Content-Type": "application/json"
    }

    # ✅ First-word clipping fix:
    # Instead of " ... " use a spoken buffer word so audio starts properly.
    # You can change "So." to "Alright." if you want.
    safe_text = "So. " + text.strip()

    payload = {
        "version": getattr(config, "HUME_TTS_VERSION", "2"),
        "utterances": [
            {
                "text": safe_text,
                "voice": {"id": voice_id}
            }
        ]
    }

    r = requests.post(url, headers=headers, json=payload, stream=True, timeout=(10, 180))

    if r.status_code != 200:
        raise Exception(f"Hume TTS failed: {r.status_code}\n{r.text}")

    audio_bytes = bytearray()

    for raw_line in r.iter_lines(decode_unicode=True):
        if not raw_line:
            continue

        line = raw_line.strip()
        if line.startswith("data:"):
            line = line[len("data:"):].strip()

        if line == "[DONE]":
            break

        try:
            obj = json.loads(line)
        except Exception:
            continue

        # Main expected format:
        # {"utterances":[{"audio":"<base64>"}]}
        if isinstance(obj, dict) and "utterances" in obj and isinstance(obj["utterances"], list):
            for u in obj["utterances"]:
                if isinstance(u, dict) and "audio" in u and isinstance(u["audio"], str):
                    audio_bytes += base64.b64decode(u["audio"])

        # fallback keys (safe)
        if isinstance(obj, dict) and "audio" in obj and isinstance(obj["audio"], str):
            audio_bytes += base64.b64decode(obj["audio"])

        if isinstance(obj, dict) and "audio_base64" in obj and isinstance(obj["audio_base64"], str):
            audio_bytes += base64.b64decode(obj["audio_base64"])

    if len(audio_bytes) == 0:
        raise Exception("No audio returned from Hume stream.")

    return bytes(audio_bytes)


def speak_hume(api_key: str, text: str):
    """
    Directly speaks the text (no saving WAV).
    Converts webm -> wav in temp folder and plays.
    """
    if not text or not text.strip():
        return

    ffmpeg_path = config.FFMPEG_PATH
    if not _ffmpeg_exists(ffmpeg_path):
        raise FileNotFoundError(f"ffmpeg.exe not found at: {ffmpeg_path}")

    voice_id = config.HUME_VOICE_ID

    audio_webm = hume_tts_stream_webm(api_key, text, voice_id)

    with tempfile.TemporaryDirectory() as td:
        webm_path = str(Path(td) / "temp.webm")
        wav_path = str(Path(td) / "temp.wav")

        with open(webm_path, "wb") as f:
            f.write(audio_webm)

        webm_to_wav(webm_path, wav_path, ffmpeg_path)

        winsound.PlaySound(wav_path, winsound.SND_FILENAME)
