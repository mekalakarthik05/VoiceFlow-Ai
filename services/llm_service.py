import logging
import time
from typing import List, Dict, Optional, Tuple
import ollama

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.available_models = self._fetch_available_models()
        self.default_model = "qwen3:4b" if "qwen3:4b" in self.available_models else (self.available_models[0] if self.available_models else "qwen3:4b")

    def _fetch_available_models(self) -> List[str]:
        try:
            models_response = ollama.list()
            # ollama.list() usually returns an object or dict with 'models'
            models = models_response.get("models", []) if isinstance(models_response, dict) else getattr(models_response, 'models', [])
            model_names = [model.get("name") if isinstance(model, dict) else getattr(model, 'model', '') for model in models]
            return [name for name in model_names if name]
        except Exception as e:
            logger.warning(f"Failed to fetch Ollama models: {e}")
            return ["qwen3:4b", "llama3.2:3b"]

    def _build_system_prompt(self, personality: str, explanation_mode: str) -> str:
        base = "You are VoiceFlow AI, a highly conversational, real-time voice assistant. "
        
        personality_prompts = {
            "General Assistant": "Be helpful, friendly, and concise.",
            "Technical Expert": "Provide accurate, highly technical answers. Use precise terminology.",
            "Interview Coach": "Act as an interviewer. Ask probing questions and give constructive feedback.",
            "Career Mentor": "Give professional, encouraging, and actionable career advice.",
            "Teacher": "Explain concepts clearly and patiently, as if teaching a student.",
            "Research Assistant": "Be objective, detailed, and focus on factual information and analysis."
        }
        
        explanation_prompts = {
            "Simple": "Explain everything in very simple terms, avoiding jargon. Keep it brief.",
            "Detailed": "Provide comprehensive and detailed explanations.",
            "Technical": "Do not shy away from advanced technical details.",
            "Interview Style": "Keep your responses concise, sharp, and structured like an interview answer."
        }
        
        prompt = base + personality_prompts.get(personality, personality_prompts["General Assistant"]) + " " + explanation_prompts.get(explanation_mode, explanation_prompts["Simple"]) + " Keep responses natural as they will be spoken aloud. Do not use markdown."
        return prompt

    def generate_response(
        self, 
        user_message: str, 
        conversation_history: List[Dict[str, str]], 
        model_name: str,
        personality: str,
        explanation_mode: str
    ) -> Tuple[Optional[str], float]:
        """
        Generates a conversational response using local Ollama models.
        Returns (response_text, latency)
        """
        start_time = time.time()
        try:
            system_prompt = self._build_system_prompt(personality, explanation_mode)
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(conversation_history)
            messages.append({"role": "user", "content": user_message})

            response = ollama.chat(
                model=model_name or self.default_model,
                messages=messages,
            )
            
            ai_response = response.get("message", {}).get("content")
            latency = time.time() - start_time
            return ai_response, latency
        except Exception as e:
            logger.error(f"Error during Ollama LLM completion: {e}")
            return None, 0.0

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Initializing LLM Service module.")
