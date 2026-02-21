from logger.logger import Logger

logger = Logger().get()


class RadioService:

    def __init__(self, music, llm, tts, streamer):
        self.music = music
        self.llm = llm
        self.tts = tts
        self.streamer = streamer
        logger.debug("RadioService initialized.")

    def run(self):
        logger.info("RadioService started.")

        while True:
            logger.debug("Requesting random song...")
            song = self.music.get_random_song()

            if not song:
                logger.warning("No song returned. Retrying...")
                continue

            logger.info(f"Now playing: {song.title} - {song.artist}")

            prompt = f"""
                You are a radio DJ.
                Introduce this track in 1-2 sentences.

                {song.stringify()}
                """

            try:
                logger.debug("Generating LLM introduction...")
                text = self.llm.generate(prompt)

                logger.debug("Generating TTS audio...")
                tts_file = self.tts.synthesize(text)

                logger.debug("Streaming TTS intro + track...")
                self.streamer.stream(tts_file, song.path)

                logger.info("Track streamed successfully.")

            except Exception as e:
                logger.error(f"Radio loop error: {e}")
