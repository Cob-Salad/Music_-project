from enum import Enum
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


class SearchParams(Enum):
    ALBUMS = "album"
    TRACKS = "track"




class PlaylistSongLink(SQLModel,table=True):
    song_id: str = Field(foreign_key="song.song_id", primary_key=True)
    playlist_id: int = Field(foreign_key="playlist.playlist_id", primary_key=True)

class Song(SQLModel, table=True):
    song_id: str | None = Field(default=None, primary_key=True)
    song_name: str
    artist_name: str
    album_name: str
    playlists: list["Playlist"] = Relationship(back_populates="songs", link_model=PlaylistSongLink)
    
class Playlist(SQLModel, table=True):
    playlist_id: int | None = Field(default=None, primary_key=True)
    playlist_name: str
    playlist_length: int 
    songs: list[Song] = Relationship(back_populates="playlists", link_model=PlaylistSongLink)
