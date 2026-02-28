import threading

import time

from config import RADIO_QUEUE_SIZE

from logger.logger import Logger

logger = Logger().get()

class RadioService:

    def __init__(self, music, playlist, content_generator, streamer):
        self.music = music
        self.playlist = playlist
        self.content_generator = content_generator
        self.streamer = streamer

        self.running = True
        
        self.current_track = None
        self.track_start_time = None

        logger.debug("RadioService initialized.")

    def run(self):
        logger.info("RadioService started.")
        
        threading.Thread(
            target=self._producer_loop,
            daemon=True
        ).start()
        
        threading.Thread(
            target=self._consumer_loop,
            daemon=True
        ).start()

    def _producer_loop(self):
        logger.info("Producer loop started")

        while self.running:
            # keep playlist filled
            if self._get_total_scheduled_time() > 60:
                time.sleep(2)
                continue

            self._enqueue_random_song_and_intro()

            next_track = self.playlist.peek_next()
            if (next_track.type == "segment"):
                logger.info(f"Queued segment: {next_track.title}")

            if (next_track.type == "song"):
                logger.info(f"Queued song: {next_track.title} - {next_track.artist}")

    def _consumer_loop(self):
        logger.info("Consumer loop started")
        
        while self.running:

            track = self.playlist.next_track()
            self.current_track = track
            self.track_start_time = time.monotonic()

            if not track:
                time.sleep(1)
                continue
            
            if (track.type == "segment"):
                logger.info(f"Now playing segment: {track.title}")

            if (track.type == "song"):
                logger.info(f"Now playing song: {track.title} - {track.artist}")
            
            self.playlist.play(track)
            self.streamer.stream_file(track.path)
            
            self.current_track = None
            self.track_start_time = None

    def _get_current_track_remaining(self) -> int:
        if not self.current_track or not self.track_start_time:
            return 0.0

        elapsed = time.monotonic() - self.track_start_time
        remaining = self.current_track.duration - elapsed

        return max(0.0, remaining)

    def _get_total_scheduled_time(self) -> int:
        return (
            self._get_current_track_remaining()
            + self.playlist.get_total_duration()
        )

    # ---------------------------------------------------------
    # Track Queueing
    # ---------------------------------------------------------

    def _enqueue_random_song_and_intro(self):
        song = self.music.get_random_song()
        intro_segment = self.content_generator.generate_dj_song_intro(song)

        self.playlist.enqueue_track(intro_segment)
        self.playlist.enqueue_track(song)