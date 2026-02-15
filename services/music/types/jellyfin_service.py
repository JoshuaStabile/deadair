from music.music_service import MusicService
from database import DatabaseService
from models import Song
from queries.jellyfin_queries import GET_RANDOM_TRACK

class JellyfinService(MusicService):

    def __init__(self, db: DatabaseService):
        self.db = db

    def get_random_track(self):
        rows = self.db.execute(GET_RANDOM_TRACK)

        if not rows:
            return None

        row = rows[0]

        return Song(
            title=row["Name"],
            album=row["Album"],
            artist=row["Artists"],
            path=row["Path"]
        )
