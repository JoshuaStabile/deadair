import subprocess
import threading
from config import ICECAST_URL
from logger.logger import Logger

logger = Logger().get()


class StreamService:

    def __init__(self):
        self.process = None
        self.lock = threading.Lock()
        self._start_encoder()

    # -------------------------
    # Start persistent encoder
    # -------------------------
    def _start_encoder(self):
        logger.info("Starting persistent FFmpeg encoder...")

        cmd = [
            "ffmpeg",
            "-re",
            "-f", "s16le",
            "-ar", "44100",
            "-ac", "2",
            "-i", "pipe:0",
            "-c:a", "libmp3lame",
            "-b:a", "320k",
            "-f", "mp3",
            ICECAST_URL
        ]

        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            bufsize=0
        )

    # ------------------------------------
    # Public function: stream file to icecast
    # ------------------------------------
    def stream_file(self, path: str):
        logger.info(f"Streaming file: {path}")

        decode_cmd = [
            "ffmpeg",
            "-i", path,
            "-f", "s16le",
            "-ar", "44100",
            "-ac", "2",
            "pipe:1"
        ]

        with subprocess.Popen(
            decode_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        ) as decoder:

            while True:
                chunk = decoder.stdout.read(4096)

                if not chunk:
                    break

                self._write_pcm(chunk)

    # -------------------------
    # Internal write to encoder
    # -------------------------
    def _write_pcm(self, pcm_bytes: bytes):
        try:
            with self.lock:
                self.process.stdin.write(pcm_bytes)
                self.process.stdin.flush()
        except BrokenPipeError:
            logger.warning("Encoder died. Restarting...")
            self._start_encoder()