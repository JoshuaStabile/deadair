import threading

import time

from config import RADIO_QUEUE_SIZE

from logger.logger import Logger

logger = Logger().get()

class RadioService:

    def __init__(self, playlist, content_generator, streamer):
        self.playlist = playlist
        self.content_generator = content_generator
        self.streamer = streamer

        self.running = True
        
        self.song_start_time = None

        logger.debug("RadioService initialized.")

    def run(self):
        logger.info("RadioService started.")

        while (self.running):
            self.playlist.fill_if_needed()
            
            song = self.playlist.next_song()
            if not song:
                time.sleep(2)
                continue

            self._play_song(song)
            
    # ---------------------------------------------------------
    # Song Playback
    # ---------------------------------------------------------

    def _play_song(self, song):

        self.playlist.current_song = song
        self.song_start_time = time.monotonic()

        # Generate DJ intro
        intro_file = self.content_generator.generate_dj_song_intro(song)

        if intro_file:
            self.streamer.stream_file(intro_file)

        # Stream music
        self.streamer.stream_file(song.path)

        logger.info(f"Now playing: {song.title}")
        # Start lookahead watcher
        self._wait_for_lookahead(song)

    # ---------------------------------------------------------
    # Lookahead Generation
    # ---------------------------------------------------------

    def _wait_for_lookahead(self, song):

        duration = song.get_duration_seconds()

        generation_started = False

        while self.running:

            elapsed = time.monotonic() - self.song_start_time
            remaining = duration - elapsed

            if remaining <= 60 and not generation_started:
                generation_started = True

                # Generate next DJ segment in background
                threading.Thread(
                    target=self._prefetch_next_content,
                    daemon=True
                ).start()

            if remaining <= 0:
                break

            time.sleep(1)

    # ---------------------------------------------------------
    # Background Prefetch
    # ---------------------------------------------------------

    def _prefetch_next_content(self):
        """Pre-warm next DJ content while current song finishes."""
        with self.generation_lock:
            try:
                next_song = self.playlist.peek_next()

                if next_song:
                    logger.info("Pre-generating next DJ content")
                    self.content_generator.generate_dj_segment(next_song)

            except Exception as e:
                logger.error(f"Prefetch failed: {e}")