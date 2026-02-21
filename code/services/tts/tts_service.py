import subprocess
from config import PIPER_MODEL_PATH, PIPER_OUTPUT_FILE

class TTSService:

    def synthesize(self, text: str) -> str:
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

        return PIPER_OUTPUT_FILE
