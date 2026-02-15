from dataclasses import dataclass


@dataclass
class Song:
    title: str
    album: str
    artist: str
    path: str