import requests

API = "https://api.spotify.com"


def get_token(token, client_id, client_secret):
    query = requests.post("https://accounts.spotify.com/api/token", {
        "refresh_token": token,
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret
    })
    return query.json()["access_token"]


def get_track_id_spotify(music, token):
    query = "q=" + music + "&type=track"
    spotify = requests.get(API + "/v1/search?" + query, headers={"Authorization": "Bearer " + token})

    result = spotify.json()["tracks"]["items"]
    if len(result) > 0:
        return result[0]["uri"]

    return None


def track_already_exist(track, playlist_id, i, token):
    request = "?market=FR&fields=items(track(uri)),total&offset=" + str(i)
    spotify = requests.get(API + "/v1/playlists/" + playlist_id + "/tracks" + request,
                           headers={"Authorization": "Bearer " + token})
    exist = False
    result = spotify.json()
    for item in result["items"]:
        if item["track"]["uri"] == track:
            exist = True

    if result["total"] > i and exist is False:
        return track_already_exist(track, playlist_id, i + 100, token)
    else:
        return exist


def add_music_to_playlist(track, playlist_id, token):
    spotify = requests.post(API + "/v1/playlists/" + playlist_id + "/tracks?uris=" + track,
                            headers={
                                "Authorization": "Bearer " + token})
    print(spotify.json())
