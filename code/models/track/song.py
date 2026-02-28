from .track import Track 

class Song(Track):
    def __init__(self, title, album, artist, duration, path):
        super().__init__(title, path, duration, "song")
        self.album = album
        self.artist = artist

    def stringify(self) -> str:
        return (
            f"Title: {self.title}\n"
            f"Artist: {self.artist}\n"
            f"Duration: {self.duration} seconds\n"
            f"Album: {self.album}"
        )