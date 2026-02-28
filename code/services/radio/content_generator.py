import soundfile as sf

from models.track.segment import Segment
from logger.logger import Logger

logger = Logger().get()

class ContentGenerator:

    def __init__(self, llm, tts, dj_service):
        self.llm = llm
        self.tts = tts
        self.dj_service = dj_service

    def get_duration_soundfile(self, file_path):
        f = sf.SoundFile(file_path)
        duration = f.frames / f.samplerate
        return duration

    def generate_dj_song_intro(self, song):
        logger.debug("Entering ContentGenerator generate_dj_song_intro")
        dj = self.dj_service.get_random_dj()

        prompt = dj.generate_intro_prompt(song)

        text = self.llm.generate(prompt)

        tts_file = self.tts.synthesize(
            model=dj.voice_model_path,
            text=text,
        )
        
        segment = Segment(
            song.title + " - intro",
            tts_file,
            self.get_duration_soundfile(tts_file),
            text
        )

        logger.debug("Exiting ContentGenerator generate_dj_song_intro")
        return segment
    
    def generate_dj_segment(self):
        logger.debug("Entering ContentGenerator generate_dj_segment")
        dj = self.dj_service.get_random_dj()

        prompt = dj.generate_segment_prompt()

        text = self.llm.generate(prompt)

        tts_file = self.tts.synthesize(
            model=dj.voice_model_path,
            text=text,
        )
        
        segment = Segment(
            "dj segment",
            tts_file,
            self.get_duration_soundfile(tts_file),
            text
        )

        logger.debug("Exiting ContentGenerator generate_dj_segment")
        return segment