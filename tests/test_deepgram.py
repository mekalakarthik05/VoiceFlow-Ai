import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.deepgram_service import STTService

class TestSTTService(unittest.TestCase):
    @patch('services.deepgram_service.faster_whisper.WhisperModel')
    @patch('services.deepgram_service.DeepgramClient')
    def test_transcribe_audio_bytes_whisper_fallback(self, mock_dg_client, mock_whisper_model):
        # Setup mocks
        mock_dg = MagicMock()
        mock_dg_client.return_value = mock_dg
        # Force Deepgram to fail
        mock_dg.listen.rest.v.return_value.transcribe_file.side_effect = Exception("API Error")
        
        # Setup Whisper fallback
        mock_whisper = MagicMock()
        mock_whisper_model.return_value = mock_whisper
        
        mock_segment = MagicMock()
        mock_segment.text = "Hello whisper fallback"
        mock_info = MagicMock()
        mock_info.language_probability = 0.99
        mock_whisper.transcribe.return_value = ([mock_segment], mock_info)

        service = STTService(api_key="fake_key")
        transcript, latency, confidence, engine = service.transcribe_audio_bytes(b"fake_audio")

        self.assertEqual(transcript, "Hello whisper fallback")
        self.assertEqual(engine, "Whisper")

if __name__ == '__main__':
    unittest.main()
