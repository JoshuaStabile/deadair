from abc import ABC, abstractmethod

class Track(ABC):
    def __init__(self, title: str, duration: float, path: str, type = "track"):
        self.type = type
        self.title = title
        self.duration = duration
        self.path = path