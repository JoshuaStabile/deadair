import requests
from config import OLLAMA_URL, OLLAMA_MODEL
from logger.logger import Logger

logger = Logger().get()


class LLMService:

    def generate(self, prompt: str) -> str:
        logger.debug(f"Entering LLMService 'generate'")

        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )

            response.raise_for_status()
            data = response.json()

            logger.debug("LLM response received successfully.")
            logger.debug("LLM response: " + data.get("response", ""))
            logger.debug(f"Exiting LLMService 'generate'")
            return data.get("response", "")

        except Exception as e:
            logger.error(f"LLM request failed: {e}")
            raise
