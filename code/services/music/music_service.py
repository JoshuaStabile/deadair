from abc import ABC, abstractmethod

class MusicService(ABC):

    @abstractmethod
    def get_random_track(self):
        pass
