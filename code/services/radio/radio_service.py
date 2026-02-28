import threading
from queue import Queue, Empty
import time
from collections import deque

from config import RADIO_QUEUE_SIZE

from logger.logger import Logger

logger = Logger().get()


class RadioService:

    def __init__(self, music, llm, tts, streamer):
        self.music = music
        self.llm = llm
        self.tts = tts
        self.streamer = streamer

        self.queue = Queue(maxsize=RADIO_QUEUE_SIZE)

        self.running = True

        # Playback state
        self.current_song = None
        self.song_start_time = 0

        # Prevent repeat songs
        self.recent_songs = deque(maxlen=10)

        # Concurrency safety
        self.generation_lock = threading.Lock()

        logger.debug("RadioService initialized.")

    # ---------------------------------------------------------
    # Producer = Playlist filling only
    # ---------------------------------------------------------

    def producer(self):
        logger.info("Producer started.")

        while self.running:
            try:
                # Maintain half-buffer fullness
                if self.queue.qsize() < RADIO_QUEUE_SIZE // 2:
                    song = self.music.get_random_song()

                    if not song:
                        logger.warning("No song returned. Retrying...")
                        time.sleep(2)
                        continue

                    # Prevent repeats
                    if song in self.recent_songs:
                        continue

                    self.queue.put(song)
                    self.recent_songs.append(song)

                    logger.info(f"Queued: {song.title}")

                else:
                    time.sleep(2)

            except Exception as e:
                logger.error(f"Producer error: {e}")
                time.sleep(2)

    # ---------------------------------------------------------
    # Consumer = Playback + Lookahead generation
    # ---------------------------------------------------------

    def consumer(self):
        logger.info("Consumer started.")

        while self.running:
            try:
                # Safe queue retrieval
                song = self.queue.get(timeout=5)

                self.current_song = song
                self.song_start_time = time.monotonic()

                logger.info(f"Now playing: {song.title}")

                # Pre-generate DJ intro + TTS
                tts_file = self._generate_next_content()

                # Stream intro + song
                if tts_file:
                    self.streamer.stream_file(tts_file)

                self.streamer.stream_file(song.path)

                # Wait while monitoring playback position
                self._wait_for_lookahead_trigger()

                self.queue.task_done()

            except Empty:
                continue

            except Exception as e:
                logger.error(f"Consumer error: {e}")

    # ---------------------------------------------------------
    # Lookahead DJ generation trigger
    # ---------------------------------------------------------

    def _wait_for_lookahead_trigger(self):
        """
        Wait until 30 seconds remain in current song,
        then begin generating next content in background.
        """

        if not self.current_song:
            return

        song_duration = self.current_song.get_duration_seconds()

        while self.running:
            elapsed = time.monotonic() - self.song_start_time
            remaining = song_duration - elapsed

            if remaining <= 30:
                logger.debug("30 second lookahead reached")

                # Only spawn generation once
                threading.Thread(
                    target=self._generate_next_content,
                    daemon=True
                ).start()

                break

            time.sleep(1)

    # ---------------------------------------------------------
    # LLM + TTS pipeline
    # ---------------------------------------------------------

    def _generate_next_content(self):
        """
        Generates DJ introduction + next track TTS.
        Uses lock to prevent multiple concurrent LLM calls.
        """

        with self.generation_lock:
            logger.info("Pre-generating next radio content")

            try:
                song = self.queue.queue[0]
            except IndexError:
                return None

            if not song:
                return None

            prompt = f"""
            You are a radio DJ. Introduce this track in 1 short sentence.

            {song.stringify()}
            """

            try:
                text = self.llm.generate(prompt)
                tts_file = self.tts.synthesize(text)

                # Pre-buffer next song
                if not self.queue.full():
                    self.queue.put(song)

                return tts_file

            except Exception as e:
                logger.error(f"Generation pipeline failed: {e}")
                return None

    # ---------------------------------------------------------
    # Main entry
    # ---------------------------------------------------------

    def run(self):
        logger.info("RadioService started.")

        producer_thread = threading.Thread(
            target=self.producer,
            daemon=True
        )

        consumer_thread = threading.Thread(
            target=self.consumer,
            daemon=True
        )

        producer_thread.start()
        consumer_thread.start()

        # Keep main thread alive
        while True:
            time.sleep(1)