from logger.logger import Logger

logger = Logger().get()

class ContentGenerator:

    def __init__(self, llm, tts, dj_service):
        self.llm = llm
        self.tts = tts
        self.dj_service = dj_service

    def generate_dj_song_intro(self, song):
        logger.debug("Entering ContentGenerator generate_dj_song_intro")
        dj = self.dj_service.get_random_dj()

        prompt = dj.generate_intro_prompt(song)

        text = self.llm.generate(prompt)

        tts_file = self.tts.synthesize(
            model=dj.voice_model_path,
            text=text,
        )

        logger.debug("Exiting ContentGenerator generate_dj_song_intro")
        return tts_file
    
    def generate_dj_segment(self):
        logger.debug("Entering ContentGenerator generate_dj_segment")
        dj = self.dj_service.get_random_dj()

        prompt = dj.generate_segment_prompt()

        text = self.llm.generate(prompt)

        tts_file = self.tts.synthesize(
            model=dj.voice_model_path,
            text=text,
        )

        logger.debug("Exiting ContentGenerator generate_dj_segment")
        return tts_file