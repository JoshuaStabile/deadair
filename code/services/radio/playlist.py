from queue import Queue
from collections import deque
from logger.logger import Logger

logger = Logger().get()

class Playlist:
    def __init__(self, music, max_size):
        self.music = music
        self.queue = Queue(maxsize=max_size)
        self.recent = deque(maxlen=10)
        
        self.current_song = None

    def fill_if_needed(self):
        if self.queue.qsize() < self.queue.maxsize // 2:
            song = self.music.get_random_song()

            if not song or song in self.recent:
                return

            logger.info(f"Buffered: {song.title}")
            self.queue_song(song)

    def queue_song(self, song):
        self.queue.put(song)
        self.recent.append(song)

    def next_song(self):
        return self.queue.get()

    def peek_next(self):
        try:
            return self.queue.queue[0]
        except IndexError:
            return None