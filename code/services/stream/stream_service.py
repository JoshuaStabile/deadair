import subprocess
import threading
from queue import Queue
from config import ICECAST_URL
from logger.logger import Logger

logger = Logger().get()


class StreamService:

    def __init__(self):
        self.lock = threading.Lock()
        self.audio_queue = Queue()

        self.running = True

        self._start_encoder()

        # Start consumer thread
        threading.Thread(
            target=self._audio_consumer,
            daemon=True
        ).start()

    # ------------------------------------------------
    # Persistent Encoder
    # ------------------------------------------------
    def _start_encoder(self):
        logger.info("Starting persistent FFmpeg encoder...")

        cmd = [
            "ffmpeg",

            "-re",

            "-f", "s16le",
            "-ar", "44100",
            "-ac", "2",

            "-i", "pipe:0",

            "-c:a", "libopus",
            "-b:a", "96k",

            "-f", "opus",

            "-content_type", "audio/ogg",

            ICECAST_URL
        ]

        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            bufsize=0
        )

    # ------------------------------------------------
    # Public API
    # ------------------------------------------------
    def stream_file(self, path):
        logger.debug("Entering StreamService stream_file")
        decode_cmd = [
            "ffmpeg",
            "-re",
            "-i", path,
            "-f", "s16le",
            "-ar", "44100",
            "-ac", "2",
            "pipe:1"
        ]

        decoder = subprocess.Popen(
            decode_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )

        while self.running and (chunk := decoder.stdout.read(4096)):
            self.stream_pcm(chunk)

        decoder.terminate()
        logger.debug("Exiting StreamService stream_file")
    
    def stream_pcm(self, pcm_bytes: bytes):
        self.audio_queue.put(pcm_bytes)

    # ------------------------------------------------
    # Consumer thread
    # ------------------------------------------------
    def _audio_consumer(self):
        logger.info("Audio consumer started")

        while self.running:
            try:
                pcm = self.audio_queue.get(timeout=5)

                if pcm is None:
                    continue

                # Write continuously without locking too long
                try:
                    self.process.stdin.write(pcm)
                    self.process.stdin.flush()

                except BrokenPipeError:
                    logger.warning("Encoder died. Restarting...")
                    self._start_encoder()

            except Exception as e:
                # logger.error(f"Audio consumer error: {e}")