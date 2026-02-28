class ArcticDJ:
    def __init__(self):
        super().__init__(
            name="Arctic",
            voice_model_path="/app/resources/piper/arctic/en_US-arctic-medium.onnx",
            personality="Old man"
        )

    def generate_intro_prompt(self, song):
        return f"""
        You are a relaxed late-night jazz radio DJ.

        Speak in 1 short smooth sentence.

        {self.stringify_context(song)}
        """