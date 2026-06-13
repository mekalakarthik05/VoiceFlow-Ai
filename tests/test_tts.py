import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.tts_service import TTSService

class TestTTSService(unittest.TestCase):
    @patch('services.tts_service.requests.get')
    @patch('services.tts_service.os.path.exists')
    @patch('services.tts_service.PiperVoice.load')
    @patch('services.tts_service.wave.open')
    @patch('services.tts_service.tempfile.NamedTemporaryFile')
    @patch('services.tts_service.pyttsx3.init')
    def test_generate_audio_success(self, mock_pyttsx3_init, mock_tempfile, mock_wave_open, mock_piper_load, mock_exists, mock_requests_get):
        # Assume model exists so it doesn't try to download
        mock_exists.return_value = True
        
        # Mock pyttsx3
        mock_pyttsx3_init.return_value = MagicMock()
        
        # Mock PiperVoice
        mock_voice_instance = MagicMock()
        mock_piper_load.return_value = mock_voice_instance
        
        # Mock tempfile
        mock_temp = MagicMock()
        mock_temp.name = "/tmp/fake.wav"
        mock_tempfile.return_value = mock_temp

        service = TTSService()
        result, latency, engine = service.generate_audio("Hello", "Female Voice")

        self.assertEqual(result, "/tmp/fake.wav")
        self.assertEqual(engine, "Piper")
        mock_voice_instance.synthesize_wav.assert_called_once()
        mock_requests_get.assert_not_called()

if __name__ == '__main__':
    unittest.main()
