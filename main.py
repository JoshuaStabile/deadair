from .code.services.database.types.sqlite3_db import SQLiteDatabase
from .code.services.music.types.jellyfin_service import JellyfinService
from .code.services.llm.llm_service import LLMService
from .code.services.tts.tts_service import TTSService
from .code.services.stream.stream_service import StreamService
from .code.services.radio.radio_service import RadioService
from .code.logger.logger import Logger

import subprocess

logger = Logger().get()

def main():
    logger.info("Application starting")
    
    subprocess.run([
        "piper",
        "--model", "./resources/piper/en_US-arctic-medium.onmx",
        "--text", "Hello world",
        "--out", "/log/output.wav"
    ])
    
    db = SQLiteDatabase()
    music = JellyfinService(db)
    llm = LLMService()
    tts = TTSService()
    streamer = StreamService()

    radio = RadioService(music, llm, tts, streamer)
    radio.run()
    logger.info("Exiting main")

if __name__ == "__main__":
    main()