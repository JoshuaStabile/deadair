from services.database import DatabaseService
from services.music import JellyfinService
from services.llm import LLMService
from services.tts import TTSService
from services.stream import StreamService
from services.radio import RadioService
from logger.logger import Logger


logger = Logger().get()

def main():
    logger.info("Application starting")
    db = DatabaseService()
    music = JellyfinService(db)
    llm = LLMService()
    tts = TTSService()
    streamer = StreamService()

    radio = RadioService(music, llm, tts, streamer)
    radio.run()
    logger.info("Exiting main")

if __name__ == "__main__":
    main()