from typing import Optional

import requests

API = "https://api.spotify.com"


class Spotify:
    def __init__(self, token: str, client_id: str, client_secret: str):
        """
        Create a new instance of spotify

        :param token: the spotify token
        :param client_id:  client id of the spotify app
        :param client_secret: client secret of the spotify app
        """
        self.__token = token
        self.__client_id = client_id
        self.__client_secret = client_secret

    def __generate_token(self) -> str:
        """
        Generate a new token for spotify with the refresh token

        :return: the new token
        """
        query = requests.post("https://accounts.spotify.com/api/token", {
            "refresh_token": self.__token,
            "grant_type": "refresh_token",
            "client_id": self.__client_id,
            "client_secret": self.__client_secret
        })
        return query.json()["access_token"]

    def get_track_id_spotify(self, title: str, artist: str) -> Optional[str]:
        """
        With a title and the artist, search over the spotify api the good track and return it

        :param title: title of the music to find
        :param artist: artist of the music to find
        :return: spotify track id
        """
        query = "q=" + title + " " + artist + "&type=track"
        spotify = requests.get(API + "/v1/search?" + query,
                               headers={"Authorization": "Bearer " + self.__generate_token()})

        result = spotify.json()["tracks"]["items"]

        if len(result) > 0:
            return result[0]["uri"]
        else:
            print("No value found for " + title + " " + artist)
        return None

    def track_already_exist(self, track, playlist_id, i):
        """
        Detect if a track is present in the specific playlist

        :param track: the spotify track id
        :param playlist_id: the spotify playlist id
        :param i: iteration for search over all playlist
        :return: True if the track is on the playlist, else return False
        """
        request = "?market=FR&fields=items(track(uri)),total&offset=" + str(i)
        spotify = requests.get(API + "/v1/playlists/" + playlist_id + "/tracks" + request,
                               headers={"Authorization": "Bearer " + self.__generate_token()})

        result = spotify.json()

        exist = False

        for item in result["items"]:
            if item["track"]["uri"] == track:
                exist = True

        if result["total"] > i and exist is False:
            return self.track_already_exist(track, playlist_id, i + 100)
        else:
            return exist

    def add_music_to_playlist(self, track: str, playlist_id: str) -> None:
        """
        Add the track to the spotify playlist

        :param track: the spotify track id
        :param playlist_id: the spotify playlist id
        """
        requests.post(API + "/v1/playlists/" + playlist_id + "/tracks?uris=" + track,
                      headers={"Authorization": "Bearer " + self.__generate_token()})
