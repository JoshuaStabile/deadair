from .track import Track

class Segment(Track):
    def __init__(self, title, path, duration, text):
        super().__init__(title, path, duration, "segment")
        self.text = text