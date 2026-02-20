class Song:
    def __init__(self, title, album, artist, path):
        self.title = title
        self.album = album
        self.artist = artist
        self.path = path

    def stringify(self) -> str:
        return (
            f"Title: {self.title}\n"
            f"Artist: {self.artist}\n"
            f"Album: {self.album}"
        )
