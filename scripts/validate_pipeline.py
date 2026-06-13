import os
import wave

print("=== Full Pipeline Validation ===\n")

# 1. STT Service
print("[1/3] Testing STT Service...")
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.deepgram_service import STTService
stt = STTService()
dg_status = "OK" if stt.deepgram_available else "UNAVAILABLE"
w_status = "OK" if stt.whisper_available else "UNAVAILABLE"
print(f"  Deepgram:       {dg_status}")
print(f"  Faster-Whisper: {w_status}")

# 2. TTS Service
print("\n[2/3] Testing TTS Service...")
from services.tts_service import TTSService
tts = TTSService()
piper_status = "OK" if tts.piper_available else "UNAVAILABLE"
pyttsx3_status = "OK" if tts.pyttsx3_available else "UNAVAILABLE"
print(f"  Piper TTS: {piper_status}")
print(f"  pyttsx3:   {pyttsx3_status}")

if tts.piper_available:
    path, lat, engine = tts.generate_audio("Testing the pipeline.", "Female Voice")
    if path and os.path.exists(path):
        with wave.open(path) as wf:
            ch = wf.getnchannels()
            rate = wf.getframerate()
            frames = wf.getnframes()
        os.remove(path)
        print(f"  Piper audio: channels={ch}, rate={rate}, frames={frames}, latency={lat:.2f}s -> PASS")
    else:
        print("  Piper audio: FAILED - no file generated")

# 3. LLM Service
print("\n[3/3] Testing LLM Service...")
from services.llm_service import LLMService
llm = LLMService()
print(f"  Ollama models: {llm.available_models}")
llm_ok = len(llm.available_models) > 0
print(f"  Ollama: {'OK' if llm_ok else 'UNAVAILABLE'}")

print("\n=== Summary ===")
print(f"  STT (Deepgram):       {dg_status}")
print(f"  STT (Whisper):        {w_status}")
print(f"  TTS (Piper):          {piper_status}")
print(f"  TTS (pyttsx3):        {pyttsx3_status}")
print(f"  LLM (Ollama):         {'OK' if llm_ok else 'UNAVAILABLE'}")
print("\nAll services initialized. Ready to launch Streamlit.\n")
