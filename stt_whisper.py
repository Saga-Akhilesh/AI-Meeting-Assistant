import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import config
_model = None

_model = None

def get_model():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel("tiny", device="cpu", compute_type="int8")
    return _model


def record_mic_wav(seconds=6):
    device = getattr(config, "MIC_DEVICE_INDEX", None)
    if device is None:
        device = sd.default.device[0]

    dev_info = sd.query_devices(device, "input")
    samplerate = int(dev_info["default_samplerate"])  # ✅ use supported rate

    print("🎙 Listening... Mic =", dev_info["name"])
    print("✅ Using sample rate:", samplerate)

    audio = sd.rec(
        int(seconds * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype=np.int16,
        device=device
    )
    sd.wait()

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(tmp.name, samplerate, audio)
    print("✅ Recorded:", tmp.name)
    return tmp.name

def transcribe_wav(path: str) -> str:
    model = get_model()
    segments, info = model.transcribe(path, vad_filter=True)
    text = " ".join([s.text for s in segments]).strip()
    return text

