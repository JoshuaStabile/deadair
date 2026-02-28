from abc import ABC, abstractmethod

class DJ(ABC):
    def __init__(self, name: str, voice_model_path: str, personality: str):
        self.name = name
        self.voice_model_path = voice_model_path
        self.personality = personality

    @abstractmethod
    def generate_intro_prompt(self, song) -> str:
        """Return prompt text for LLM generation"""
        pass

    def stringify_context(self, song) -> str:
        return f"""
        DJ Name: {self.name}
        Personality: {self.personality}

        Song Info:
        {song.stringify()}
        """