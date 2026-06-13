import logging
import os
import requests
import tempfile
import wave
import time
from typing import Optional, Tuple
from piper.voice import PiperVoice
import pyttsx3

logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        self.model_name = "en_US-lessac-low"
        self.model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "models")
        os.makedirs(self.model_dir, exist_ok=True)
        
        self.model_path = os.path.join(self.model_dir, f"{self.model_name}.onnx")
        self.config_path = os.path.join(self.model_dir, f"{self.model_name}.onnx.json")
        
        self.piper_available = False
        self.voice = None
        
        try:
            self._ensure_model_exists()
            self.voice = PiperVoice.load(self.model_path, config_path=self.config_path)
            self.piper_available = True
            logger.info("Piper TTS initialized.")
        except Exception as e:
            logger.warning(f"Piper TTS initialization failed: {e}")

        # Initialize pyttsx3 fallback
        self.pyttsx3_available = False
        try:
            self.pyttsx3_engine = pyttsx3.init()
            self.pyttsx3_available = True
            logger.info("pyttsx3 fallback initialized.")
        except Exception as e:
            logger.warning(f"pyttsx3 fallback initialization failed: {e}")

    def _ensure_model_exists(self):
        base_url = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/low"
        if not os.path.exists(self.model_path):
            logger.info("Downloading Piper model...")
            self._download_file(f"{base_url}/en_US-lessac-low.onnx", self.model_path)
        if not os.path.exists(self.config_path):
            logger.info("Downloading Piper config...")
            self._download_file(f"{base_url}/en_US-lessac-low.onnx.json", self.config_path)

    def _download_file(self, url: str, dest_path: str):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    def generate_audio(self, text: str, voice_type: str = "Female Voice") -> Tuple[Optional[str], float, str]:
        start_time = time.time()
        
        # Prefer Piper for natural/female. 
        use_piper = self.piper_available and voice_type in ["Female Voice", "Natural Voice"]
        
        if use_piper:
            try:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                temp_file.close()
                with wave.open(temp_file.name, "w") as wav_file:
                    self.voice.synthesize_wav(text, wav_file)
                latency = time.time() - start_time
                return temp_file.name, latency, "Piper"
            except Exception as e:
                logger.error(f"Piper TTS failed: {e}")

        if self.pyttsx3_available:
            try:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                temp_file.close()
                
                voices = self.pyttsx3_engine.getProperty('voices')
                if voice_type == "Male Voice" and len(voices) > 0:
                    self.pyttsx3_engine.setProperty('voice', voices[0].id)
                elif voice_type == "Female Voice" and len(voices) > 1:
                    self.pyttsx3_engine.setProperty('voice', voices[1].id)
                
                rate = 200 if voice_type == "Fast Voice" else 150
                self.pyttsx3_engine.setProperty('rate', rate)

                self.pyttsx3_engine.save_to_file(text, temp_file.name)
                self.pyttsx3_engine.runAndWait()
                
                latency = time.time() - start_time
                return temp_file.name, latency, "Pyttsx3"
            except Exception as e:
                logger.error(f"Pyttsx3 fallback failed: {e}")
                
        return None, 0.0, "None"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Initializing TTS Service module.")
