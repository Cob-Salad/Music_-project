# Music Project
### Bringing Spotify API and your personal databases together.
### Gives the ability to intake song information from Spotify's API so you can create your own playlists.

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
