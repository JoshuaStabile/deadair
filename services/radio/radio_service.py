import models.song

class RadioService:

    def __init__(self, music, llm, tts, streamer):
        self.music = music
        self.llm = llm
        self.tts = tts
        self.streamer = streamer

    def run(self):
        while True:
            song = self.music.get_random_song()
            if not song:
                continue

            prompt = f"""
                You are a radio DJ.
                Introduce this track in 1-2 sentences.

                {song.stringify}
            """

            text = self.llm.generate(prompt)
            tts_file = self.tts.synthesize(text)
            self.streamer.stream(tts_file, song["path"])
