class Song:
    def __init__(self, title, album, artist, ticks, path):
        self.title = title
        self.album = album
        self.artist = artist
        self.ticks = ticks
        self.seconds = ticks / 10_000_000
        self.path = path

    def stringify(self) -> str:
        return (
            f"Title: {self.title}\n"
            f"Artist: {self.artist}\n"
            f"Ticks: {self.ticks}\n"
            f"Album: {self.album}"
        )