from services.database.db import ConnectionMode
from services.database.types.sqlite3_db import SQLiteDatabase
from services.music.types.jellyfin_service import JellyfinService
from services.llm.llm_service import LLMService
from services.tts.tts_service import TTSService
from services.stream.stream_service import StreamService
from services.radio.radio_service import RadioService
from services.radio.playlist import Playlist
from services.radio.content_generator import ContentGenerator
from services.dj.dj_service import DJService
from services.dj.types.arctic import ArcticDJ

from logger.logger import Logger

from config import (
    JELLYFIN_DB_PATH,
)

logger = Logger().get()

def main():
    logger.info("Application starting")
    
    if not JELLYFIN_DB_PATH:
        raise RuntimeError("JELLYFIN_DB_PATH not set")
    
    db = SQLiteDatabase(JELLYFIN_DB_PATH, mode=ConnectionMode.THREAD_LOCAL)
    
    music_service = JellyfinService(db)
    playlist = Playlist(music_service, 2)
    
    llm_service = LLMService()
    tts_service = TTSService()
    dj_service = DJService([
        ArcticDJ
    ])
    
    content_generator = ContentGenerator(llm_service, tts_service, dj_service)
    
    streamer = StreamService()

    radio = RadioService(playlist, content_generator, streamer)
    radio.run()
    logger.info("Exiting main")

if __name__ == "__main__":
    main()