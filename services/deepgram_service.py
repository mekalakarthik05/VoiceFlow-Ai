import logging
import os
import time
from typing import Optional, Tuple
from dotenv import load_dotenv

from deepgram import DeepgramClient
import faster_whisper
import tempfile

load_dotenv()
logger = logging.getLogger(__name__)

class STTService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DEEPGRAM_API_KEY")
        self.dg_client = None
        self.whisper_model = None
        
        self.deepgram_available = False
        self.whisper_available = False
        
        if self.api_key:
            try:
                # deepgram-sdk v7+: api_key is keyword-only in BaseClient
                self.dg_client = DeepgramClient(api_key=self.api_key)
                self.deepgram_available = True
                logger.info("Deepgram initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize Deepgram: {e}")
        
        # Initialize Faster-Whisper fallback
        try:
            # use "tiny" for speed, cpu/int8 for compatibility
            self.whisper_model = faster_whisper.WhisperModel("tiny", device="cpu", compute_type="int8")
            self.whisper_available = True
            logger.info("Faster-Whisper fallback initialized successfully.")
        except Exception as e:
            logger.warning(f"Failed to initialize Faster-Whisper: {e}")

    def _transcribe_with_deepgram(self, audio_data: bytes, mapped_lang: str) -> Optional[Tuple[str, float]]:
        """
        Calls Deepgram REST API using deepgram-sdk v7.3.1 API.
        Returns (transcript, confidence) or None on failure.
        
        SDK v7 API:
          client.listen.v1.media.transcribe_file(
              request=<bytes>,
              model="nova-2",
              smart_format=True,
              language="en"
          )
        Response: ListenV1Response (Pydantic model)
          .results.channels[0].alternatives[0].transcript
          .results.channels[0].alternatives[0].confidence

        Runs in a separate thread to avoid RuntimeError: Event loop is closed
        that can occur when Streamlit's asyncio loop conflicts with httpx internals.
        """
        import threading

        result_holder = [None]
        error_holder = [None]

        def _call():
            try:
                response = self.dg_client.listen.v1.media.transcribe_file(
                    request=audio_data,
                    model="nova-2",
                    smart_format=True,
                    language=mapped_lang,
                )
                # Response is a Pydantic model — use attribute access, not .get()
                channels = response.results.channels
                if channels and len(channels) > 0:
                    alternatives = channels[0].alternatives
                    if alternatives and len(alternatives) > 0:
                        transcript = alternatives[0].transcript
                        confidence = alternatives[0].confidence if hasattr(alternatives[0], 'confidence') else 0.0
                        if transcript:
                            result_holder[0] = (transcript, float(confidence or 0.0))
            except Exception as e:
                error_holder[0] = e

        t = threading.Thread(target=_call, daemon=True)
        t.start()
        t.join(timeout=30)  # 30-second timeout for transcription

        if error_holder[0] is not None:
            logger.warning(f"Deepgram transcription failed: {error_holder[0]}")
            return None

        return result_holder[0]


    def transcribe_audio_bytes(self, audio_data: bytes, language: str = "en") -> Tuple[Optional[str], float, float, str]:
        """
        Transcribes audio. Returns (transcript, latency_sec, confidence, source_engine)
        """
        start_time = time.time()
        
        lang_map = {
            "English": "en",
            "Hindi": "hi",
            "Telugu": "te"
        }
        mapped_lang = lang_map.get(language, "en")
        
        # 1. Try Deepgram
        if self.deepgram_available:
            result = self._transcribe_with_deepgram(audio_data, mapped_lang)
            if result is not None:
                transcript, confidence = result
                latency = time.time() - start_time
                return transcript, latency, confidence, "Deepgram"
                
        # 2. Fallback to Faster-Whisper
        if self.whisper_available:
            logger.info("Falling back to Faster-Whisper STT.")
            try:
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                    temp_audio.write(audio_data)
                    temp_file_path = temp_audio.name
                
                segments, info = self.whisper_model.transcribe(temp_file_path, beam_size=5, language=mapped_lang)
                transcript = " ".join([segment.text for segment in segments]).strip()
                
                os.remove(temp_file_path)
                
                if transcript:
                    latency = time.time() - start_time
                    return transcript, latency, info.language_probability, "Whisper"
            except Exception as e:
                logger.error(f"Faster-Whisper fallback failed: {e}")
                
        return None, 0.0, 0.0, "None"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Initializing STT Service module.")
