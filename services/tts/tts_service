import subprocess
from config import PIPER_MODEL_PATH, TTS_OUTPUT_FILE

class TTSService:

    def synthesize(self, text: str) -> str:
        process = subprocess.Popen(
            [
                "piper",
                "--model", PIPER_MODEL_PATH,
                "--output_file", TTS_OUTPUT_FILE
            ],
            stdin=subprocess.PIPE,
            text=True
        )

        process.communicate(text)

        return TTS_OUTPUT_FILE
