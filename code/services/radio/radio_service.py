import threading
from queue import Queue
import time

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
        
        logger.debug("RadioService initialized.")

    def producer(self):
        logger.info("Producer started.")

        while self.running:
            if self.queue.qsize() < RADIO_QUEUE_SIZE / 2:
                logger.debug("Queue low. Adding song...")

                song = self.music.get_random_song()
                if not song:
                    logger.warning("No song returned. Retrying...")
                    continue

                self.queue.put(song)
                logger.info(f"Queued: {song.title}")

            else:
                time.sleep(2)

    def consumer(self):
        logger.info("Consumer started.")

        while self.running:
            song = self.queue.get()  # blocks if empty

            logger.info(f"Now playing: {song.title} - {song.artist}")

            prompt = f"""
                You are a radio DJ.
                Introduce this track in 1-2 sentences.

                {song.stringify()}
            """

            try:
                text = self.llm.generate(prompt)
                tts_file = self.tts.synthesize(text)

                self.streamer.stream_file(tts_file)
                self.streamer.stream_file(song.path)

            except Exception as e:
                logger.error(f"Streaming error: {e}")

            self.queue.task_done()

    def run(self):
        logger.info("RadioService started.")

        producer_thread = threading.Thread(target=self.producer, daemon=True)
        consumer_thread = threading.Thread(target=self.consumer, daemon=True)

        producer_thread.start()
        consumer_thread.start()

        while True:
            time.sleep(1)
