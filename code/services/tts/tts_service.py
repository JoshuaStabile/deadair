import subprocess
from config import PIPER_MODEL_PATH, PIPER_OUTPUT_FILE
from logger.logger import Logger

logger = Logger().get()

class TTSService:

    def synthesize(self, text: str) -> str:
        logger.debug("Entering TTSService 'synthesize'")
        
        process = subprocess.Popen(
            [
                "piper",
                "--model", PIPER_MODEL_PATH,
                "--output_file", PIPER_OUTPUT_FILE
            ],
            stdin=subprocess.PIPE,
            text=True
        )

        process.communicate(text)

        logger.debug("Exiting TTSService 'synthesize'")
        return PIPER_OUTPUT_FILE
