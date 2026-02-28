from .track import Track

class Segment(Track):
    def __init__(self, title: str, path: str, duration: float, text: str):
        super().__init__(title, path, duration, "segment")
        self.text = text