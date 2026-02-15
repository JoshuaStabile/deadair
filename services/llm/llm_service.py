import requests
from config import OLLAMA_URL, OLLAMA_MODEL

class LLMService:

    def generate(self, prompt: str) -> str:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()
        return data["response"]
