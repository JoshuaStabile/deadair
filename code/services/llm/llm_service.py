import requests
from config import OLLAMA_URL, OLLAMA_MODEL
from logger.logger import Logger

logger = Logger().get()


class LLMService:

    def generate(self, prompt: str) -> str:
        logger.debug(f"Sending prompt to LLM (model={OLLAMA_MODEL})")
        logger.debug(f"Prompt preview: {prompt[:200]}")

        try:
            response = requests.post(
                OLLAMA_URL,
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
            return data.get("response", "")

        except Exception as e:
            logger.error(f"LLM request failed: {e}")
            raise
