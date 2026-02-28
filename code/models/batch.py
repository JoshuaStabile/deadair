import uuid

class Batch:
    def __init__(self, theme: str, songs: list, duration_seconds: float, intro_script: str):
        self.id = uuid.uuid4()
        self.theme = theme
        self.songs = songs
        self.duration_seconds = duration_seconds
        self.intro_script = intro_script

    def stringify(self) -> str:
        return (
            
        )
