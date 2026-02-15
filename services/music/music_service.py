from abc import ABC, abstractmethod

class SongService(ABC):

    @abstractmethod
    def get_random_track(self):
        pass
