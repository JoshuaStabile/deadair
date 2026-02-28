from ..music_service import MusicService
from services.database.db import Database
from models.track.song import Song
from queries.jellyfin_queries import GET_RANDOM_TRACK
from logger.logger import Logger

logger = Logger().get()


class JellyfinService(MusicService):

    def __init__(self, db: Database):
        self.db = db
        logger.debug("JellyfinService initialized.")

    def get_random_song(self):
        logger.debug(f"Entering JellyfinService 'get_random_song'")

        rows = self.db.fetch(GET_RANDOM_TRACK)

        if not rows:
            logger.warning("No tracks returned from database.")
            return None

        row = rows[0]

        song = Song(
            title=row["Name"],
            album=row["Album"],
            artist=row["Artists"],
            duration=self.get_duration_seconds(row["RunTimeTicks"]),
            path=row["Path"]
        )

        logger.info(f"Selected track: {song.title} - {song.artist}")
        logger.debug(f"Exiting JellyfinService 'get_random_song'")
        return song

    def get_duration_seconds(self, ticks):
        return ticks / 10_000_000