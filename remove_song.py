"""
    Author: Sloth
    Date: 9/29/2024
    Description: Python script to get the currently playing song that I'm playing and remove it from all playlists and liked songs.
"""

import spotipy
import spotipy.util as util
from dotenv import load_dotenv

import os


load_dotenv()


def remove_hype_song(
        sp: spotipy.Spotify,
        playlist_id: str,
        track: str
    ) -> None:

    sp.playlist_remove_all_occurrences_of_items(playlist_id, [track], snapshot_id=None)


def get_hype_songs(
        sp: spotipy.Spotify,
        playlist_id: str
    ) -> list[str]:

    songs: list[str] = []
    i: int = 0
    while True:
        if i == 0:
            response = sp.playlist_tracks(playlist_id)
        else:
            response = sp.next(response)

        for song in response["items"]:
            songs.append(song["track"]["id"])

        if response["next"] == None:
            return songs

        i += 1


def get_playlist_id(sp: spotipy.Spotify) -> str:
    id: str = sp.me()["id"]
    return sp.user_playlists(id)["items"][0]["id"]


def remove_saved_track(
        sp: spotipy.Spotify,
        track_id: str
    ) -> None:

    sp.current_user_saved_tracks_delete(tracks=[track_id])


def get_playing_track(sp: spotipy.Spotify) -> str:
    return sp.current_user_playing_track()["item"]["id"]


def authorize() -> spotipy.Spotify:
    client_id: str = os.getenv("CLIENT_ID")
    client_secret: str = os.getenv("CLIENT_SECRET")
    redirect_uri: str = "http://localhost:7777/callback"
    scope: str = "user-read-currently-playing user-library-modify playlist-modify-public"
    username: str = "nickbiacsi@gmail.com"

    token: str = util.prompt_for_user_token(
        username,
        scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri
    )

    return spotipy.Spotify(auth=token)


def main() -> None:
    sp = authorize()
    track: str = get_playing_track(sp)
    remove_saved_track(sp, track)
    
    playlist_id: str = get_playlist_id(sp)
    hype_songs: list[str] = get_hype_songs(sp, playlist_id)
    
    if track in hype_songs:
        remove_hype_song(sp, playlist_id, track)


if __name__ == "__main__":
    main()
