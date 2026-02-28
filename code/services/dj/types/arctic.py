from ..dj import DJ

class ArcticDJ(DJ):
    def __init__(self):
        super().__init__(
            name="Arctic",
            voice_model_path="/app/resources/piper/arctic/en_US-arctic-medium.onnx",
            personality="Old man"
        )

    def generate_intro_prompt(self, song):
        return f"""
        You are a radio DJ.
        Introduce this song in 1 short sentence.

        {self.stringify_context(song)}
        """