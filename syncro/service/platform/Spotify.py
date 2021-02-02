import requests

API = "https://api.spotify.com"


class Spotify:
    def __init__(self, token, client_id, client_secret):
        self.__token = self.generate_token(token, client_id, client_secret)

    def get_token(self):
        return self.__token

    def generate_token(self, token, client_id, client_secret):
        query = requests.post("https://accounts.spotify.com/api/token", {
            "refresh_token": token,
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret
        })
        return query.json()["access_token"]

    def get_track_id_spotify(self, title, artist):
        query = "q=" + title + " " + artist + "&type=track"
        spotify = requests.get(API + "/v1/search?" + query, headers={"Authorization": "Bearer " + self.__token})

        result = spotify.json()["tracks"]["items"]

        if len(result) > 0:
            return result[0]["uri"]
        else:
            print("No value found for " + title + " " + artist)
        return None

    def track_already_exist(self, track, playlist_id, i):
        request = "?market=FR&fields=items(track(uri)),total&offset=" + str(i)
        spotify = requests.get(API + "/v1/playlists/" + playlist_id + "/tracks" + request,
                               headers={"Authorization": "Bearer " + self.__token})

        result = spotify.json()

        exist = False

        for item in result["items"]:
            if item["track"]["uri"] == track:
                exist = True

        if result["total"] > i and exist is False:
            return self.track_already_exist(track, playlist_id, i + 100)
        else:
            return exist

    def add_music_to_playlist(self, track, playlist_id):
        requests.post(API + "/v1/playlists/" + playlist_id + "/tracks?uris=" + track,
                      headers={"Authorization": "Bearer " + self.__token})
