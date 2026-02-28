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
        
        # Concurrency safety 
        self.generation_lock = threading.Lock()

        logger.debug("RadioService initialized.")

    def run(self):
        logger.info("RadioService started.")

        while (self.running):
            self.playlist.fill_if_needed()
            
            song = self.playlist.next_song()
            if not song:
                logger.debug("No next song found...")
                time.sleep(2)
                continue

            self._play_song(song)
            
    # ---------------------------------------------------------
    # Song Playback
    # ---------------------------------------------------------

    def _play_song(self, song):
        logger.debug("Entering RadioService _play_song")

        self.song_start_time = time.monotonic()

        intro_file = self.content_generator.generate_dj_song_intro(song)

        if intro_file:
            self.streamer.stream_file(intro_file)

        # Start song streaming in background
        stream_thread = threading.Thread(
            target=self.streamer.stream_file,
            args=(song.path,),
        )
        stream_thread.start()

        logger.info(f"Now playing: {song.title}")

        # Monitor while song is playing
        self._wait_for_lookahead(song)

        # Wait for stream to finish before continuing
        stream_thread.join()

        logger.debug("Exiting RadioService _play_song")

    # ---------------------------------------------------------
    # Lookahead Generation
    # ---------------------------------------------------------

    def _wait_for_lookahead(self, song):
        logger.debug(f"Entering RadioService _wait_for_lookahead")
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
        logger.debug(f"Exiting RadioService _wait_for_lookahead")

    # ---------------------------------------------------------
    # Background Prefetch
    # ---------------------------------------------------------

    def _prefetch_next_content(self):
        """Pre-warm next DJ content while current song finishes."""
        logger.debug(f"Entering RadioService _prefetch_next_content")
        
        with self.generation_lock:
            try:
                next_song = self.playlist.peek_next()

                if next_song:
                    logger.info("Pre-generating next DJ content")
                    self.content_generator.generate_dj_segment(next_song)

            except Exception as e:
                logger.error(f"Prefetch failed: {e}")
        logger.debug(f"Exiting RadioService _prefetch_next_content")