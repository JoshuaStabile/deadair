from abc import ABC, abstractmethod

class Track(ABC):
    def __init__(self, title, duration, path, type = "track"):
        self.type = type
        self.title = title
        self.duration = duration
        self.path = path