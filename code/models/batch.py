import uuid

class Batch:
    def __init__(self, theme, songs):
        self.id = uuid.uuid4()
        self.theme = theme
        self.songs = songs

    def stringify(self) -> str:
        return (
            
        )
