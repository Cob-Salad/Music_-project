import asyncio
import spotify
from decouple import config

from fastapi import Depends, FastAPI
import requests

from sqlmodel import Session, select
from database import get_db
from models import Song, Playlist, PlaylistSongLink, SearchParams

client = spotify.Client(config('CLIENT_ID'), config('CLIENT_SECRET'))

description = """
this will help you along your way

## GET
### Any endpoint starting with /Spotify ties directly into the spotify database.
### Any endpoint starting with /Database ties to your personal database.
### When searching using the "album" parameter "search_length" does not affect the results.


## POST
### I reccomend using the search function to determine what index the song you are trying to add is.
### Adds songs directly from the spotify database to a selected playlist.
### If you set index to 0 it will put the entire search length of results into the database.
### If you set playlists to anything but 0 it will be put in a playlist of the corresponding id.
### Any of the "link" endpoints will connect song(s) to a playlist

## DELETE
### Will delete anything you ask it to regardless of if the song is in a playlist or if the playlist has songs
### Reccomended to use the in database search function to get the right song_id

"""
tags_metadata = [
    {
        "name": "Get",
        "description": "Acquire Information"
    },
    {
        "name": "Post",
        "description": "Add Information"
    },
    {
        "name": "Delete",
        "description": "Remove Things"
    }

]
app = FastAPI(
    title="Spotify Database Port",
    description=description,
    summary="Creator of Playlists, Seeker of Sound",
    version=">:P"
)



### GET ###

@app.get("/spotify/search", tags=["Get"])
async def get_search(search: str, search_parameters: SearchParams, search_length: int) -> list[Song]:
    response = await client.search(search, types=[search_parameters.value], limit=search_length)
    search_list = []
    if search_parameters == "track":
        for i in range(search_length):
            song = response.tracks[i]
            search_list.append(Song(
                song_id = song.id,
                song_name = song.name,
                artist_name = song.artist.name,
                album_name = song.album.name
            ))
    elif search_parameters.value == "album":
        album_id = response.albums[0].id
        album = await client.get_album(f'spotify:{album_id}')
        all_tracks = await album.get_all_tracks()
        for i in range(len(all_tracks)):
            song = all_tracks[i]
            search_list.append(Song(
                song_id = song.id,
                song_name = song.name,
                artist_name = song.artist.name,
                album_name = album.name
            ))
    return search_list

@app.get("/Database/songs", tags=["Get"])
async def get_all_songs(db: Session = Depends(get_db)) -> list[Song]:
    return db.exec(select(Song)).all()

@app.get("/Database/playlist/{playlist_id}", tags=["Get"])
async def get_playlist(playlist_id: int, db: Session = Depends(get_db)) -> list[Song]:
    playlist = db.get(Playlist, playlist_id)
    return playlist.songs


### POST ##

@app.post("/Database/playlists", tags=["Post"])
async def create_playlist(playlist_name: str, db: Session = Depends(get_db)):
    playlist = Playlist(
        playlist_name=playlist_name,
        playlist_length=0
            )
    playlist.songs.append()
    db.add(playlist)
    db.commit()


@app.post("/Database/songs", tags=["Post"])
async def add_songs(index: int, search: str, search_length: int, db: Session = Depends(get_db)):
    search_list = await get_search(search=search, search_length=search_length)
    db.add(search_list[index])
    db.commit()


@app.post("/Database/link", tags=["Post"])
async def add_song_playlist(playlist_id: int, song_id: str, db: Session = Depends(get_db)):
    playlist = db.get(Playlist, playlist_id)
    song = db.get(Song, song_id)
    playlist.songs.append(song)
    db.commit()

###
# I reccomend using the search function above to determine what index the song you are trying to add is.
# Adds songs directly from the spotify database to a selected playlist.
# If you set index to 0 it will put the entire search length of results into the database.
# If you set playlists to anything but 0 it will be put in a playlist of the corresponding id.
#
###
@app.post("/Database/direct_link", tags=["Post"])
async def direct_add_playlist(playlist_id: int, index: int, search:str, search_parameters: SearchParams, search_length: int, db: Session = Depends(get_db)):
    response = await client.search(search, types=[search_parameters.value], limit=search_length)
    search_list = []
    if search_parameters == "track":
        for i in range(search_length):
            song = response.tracks[i]
            search_list.append(Song(
                song_id = song.id,
                song_name = song.name,
                artist_name = song.artist.name,
                album_name = song.album.name
            ))
    elif search_parameters.value == "album":
        album_id = response.albums[0].id
        album = await client.get_album(f'spotify:{album_id}')
        all_tracks = await album.get_all_tracks()
        for i in range(len(all_tracks)):
            song = all_tracks[i]
            search_list.append(Song(
                song_id = song.id,
                song_name = song.name,
                artist_name = song.artist.name,
                album_name = album.name
            ))
    playlist = db.get(Playlist, playlist_id)
    index = index - 1
    if playlist_id == 0:
        if index == -1:
            for i in range(len(search_list)):
                db.add(search_list[i])
        else:
            db.add(search_list[index])     
    else:
        if index == -1:
            for i in range(len(search_list)):
                playlist.songs.append(search_list[i])
        else:
            playlist.songs.append(search_list[index])
    db.commit()


### DELETE ###

@app.delete("/Database/Songs", tags=["Delete"])
async def delete_song(song_ids: str, db: Session = Depends(get_db)):
    statement = select(Song).where(Song.song_id == song_ids)
    results = db.exec(statement)
    song = results.one()
    db.delete(song)
    db.commit()

@app.delete("/Database/Clear_songs", tags=["Delete"])
async def clear_songs(db: Session = Depends(get_db)):
    statement = db.exec(select(Song)).all()
    for i in range(len(statement)):
        db.delete(statement[i])
        db.commit() 
    
@app.delete("/Database/playlists", tags=["Delete"])
async def delete_playlist(id: int, db: Session = Depends(get_db)):
    statement = db.exec(select(Playlist).where(Playlist.playlist_id == id))
    playlist = statement.one()
    db.delete(playlist)
    db.commit()