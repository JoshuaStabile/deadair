import threading
from logger.logger import Logger

class Playlist:

    def __init__(self):
        self._tracks = []
        self._lock = threading.Lock()

    def enqueue_track(self, track):
        with self._lock:
            self._tracks.append(track)

    def next_track(self):
        with self._lock:
            if not self._tracks:
                return None
            return self._tracks.pop(0)

    def peek_next(self):
        with self._lock:
            return self._tracks[0] if self._tracks else None

    def get_total_duration(self):
        with self._lock:
            return sum(t.duration for t in self._tracks)