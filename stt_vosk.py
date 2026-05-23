import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import config

_model = None

def get_model():
    global _model
    if _model is None:
        _model = Model(config.VOSK_MODEL_PATH)
    return _model

def record_and_transcribe(seconds=6):
    device = getattr(config, "MIC_DEVICE_INDEX", None)
    if device is None:
        device = sd.default.device[0]

    dev_info = sd.query_devices(device, "input")
    samplerate = int(dev_info["default_samplerate"])

    print("🎙 Listening... Mic =", dev_info["name"])
    print("✅ Using sample rate:", samplerate)

    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    model = get_model()
    rec = KaldiRecognizer(model, samplerate)

    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device,
                           dtype="int16", channels=1, callback=callback):
        for _ in range(int(seconds * samplerate / 8000) + 1):
            data = q.get()
            rec.AcceptWaveform(data)

    result = json.loads(rec.FinalResult())
    return result.get("text", "").strip()
