from music.music_service import MusicService
from database import DatabaseService
from models import Song
from queries.jellyfin_queries import GET_RANDOM_TRACK
from logger.logger import Logger

logger = Logger().get()


class JellyfinService(MusicService):

    def __init__(self, db: DatabaseService):
        self.db = db
        logger.debug("JellyfinService initialized.")

    def get_random_song(self):
        logger.debug("Fetching random track from Jellyfin database.")

        rows = self.db.execute(GET_RANDOM_TRACK)

        if not rows:
            logger.warning("No tracks returned from database.")
            return None

        row = rows[0]

        song = Song(
            title=row["Name"],
            album=row["Album"],
            artist=row["Artists"],
            path=row["Path"]
        )

        logger.info(f"Selected track: {song.title} - {song.artist}")
        return song
