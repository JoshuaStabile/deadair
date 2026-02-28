class Song:
    def __init__(self, title, album, artist, ticks, path):
        self.title = title
        self.album = album
        self.artist = artist
        self.ticks = ticks
        self.path = path

    def get_duration_seconds(self):
        return self.ticks / 10_000_000

    def stringify(self) -> str:
        return (
            f"Title: {self.title}\n"
            f"Artist: {self.artist}\n"
            f"Ticks: {self.ticks}\n"
            f"Album: {self.album}"
        )