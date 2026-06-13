import unittest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.llm_service import LLMService

class TestLLMService(unittest.TestCase):
    @patch('services.llm_service.ollama')
    def test_generate_response_success(self, mock_ollama):
        mock_ollama.chat.return_value = {
            "message": {
                "content": "Hello, I am local AI."
            }
        }
        mock_ollama.list.return_value = {"models": [{"name": "qwen3:4b"}]}

        service = LLMService()
        result, latency = service.generate_response("How are you?", [], "qwen3:4b", "General Assistant", "Simple")

        self.assertEqual(result, "Hello, I am local AI.")
        self.assertGreaterEqual(latency, 0.0)
        mock_ollama.chat.assert_called_once()

if __name__ == '__main__':
    unittest.main()
