import datetime
import os
import time

import requests
from bs4 import BeautifulSoup

API = "https://api.spotify.com/v1"
URL = "https://www.6play.fr/rtl2/quel-est-ce-titre"

TOKEN = os.getenv("token")
CLIENT_ID = os.getenv("client_id")
CLIENT_SECRET = os.getenv("client_secret")

print("Run with")
print("Token        = " + TOKEN)
print("ClientId     = " + CLIENT_ID)
print("ClientSecret = " + CLIENT_SECRET)
print(" ")


def get_token():
    query = requests.post("https://accounts.spotify.com/api/token", {
        "refresh_token": TOKEN,
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    return query.json()["access_token"]


def get_last_music():
    page = requests.get(URL)
    musics = []

    html_body = BeautifulSoup(page.content, "html.parser")
    html_music = html_body.findAll(class_="ecfper-4 dswJZp")

    for music in html_music:
        title = music.find(class_="ecfper-5 cLjpFE").text
        author = music.find(class_="ecfper-6 cLqSnv").text
        musics.append(title + " " + author)

    return musics


def get_track_id_spotify(music, token):
    query = "q=" + music + "&type=track"
    spotify = requests.get(API + "/search?" + query, headers={"Authorization": "Bearer " + token})

    result = spotify.json()["tracks"]["items"]
    if len(result) > 0:
        return result[0]["uri"]

    return None


def track_already_exist(track, i, token):
    request = "?market=FR&fields=items(track(uri)),total&offset=" + str(i)
    spotify = requests.get(API + "/playlists/6iazs8VECddcN2EtJFDhVA/tracks" + request,
                           headers={"Authorization": "Bearer " + token})
    exist = False
    result = spotify.json()
    for item in result["items"]:
        if item["track"]["uri"] == track:
            exist = True

    if result["total"] > i and exist is False:
        return track_already_exist(track, i + 100, token)
    else:
        return exist


def add_music_to_playlist(track, token):
    spotify = requests.post(API + "/playlists/6iazs8VECddcN2EtJFDhVA/tracks?uris=" + track,
                            headers={
                                "Authorization": "Bearer " + token})
    print(spotify.json())


def run():
    token = get_token()
    print("Run at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    musics = get_last_music()

    for music in musics:
        track_id = get_track_id_spotify(music, token)

        if track_id is not None:
            if not track_already_exist(track_id, 0, token):
                add_music_to_playlist(track_id, token)
        else:
            log = open("log.txt", "a")
            log.write("Can't find the music " + music + "\n")

    time.sleep(600)
    run()


run()
