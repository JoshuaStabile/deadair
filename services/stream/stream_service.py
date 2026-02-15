import subprocess
from config import ICECAST_URL

class StreamService:

    def stream(self, tts_file: str, track_path: str):
        cmd = [
            "ffmpeg",
            "-re",
            "-i", tts_file,
            "-i", track_path,
            "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[out]",
            "-map", "[out]",
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            "-f", "mp3",
            ICECAST_URL
        ]

        subprocess.run(cmd)
