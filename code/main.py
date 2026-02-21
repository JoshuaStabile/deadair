from services.database.types.sqlite3_db import SQLiteDatabase
from services.music.types.jellyfin_service import JellyfinService
from services.llm.llm_service import LLMService
from services.tts.tts_service import TTSService
from services.stream.stream_service import StreamService
from services.radio.radio_service import RadioService
from logger.logger import Logger

from config import (
    PIPER_MODEL_PATH,
    PIPER_OUTPUT_FILE
)

import subprocess

logger = Logger().get()

def main():
    logger.info("Application starting")
    
    subprocess.run([
        "piper",
        "--model", PIPER_MODEL_PATH,
        "--text", "Hello world",
        "--out", PIPER_OUTPUT_FILE
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