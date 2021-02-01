import datetime
import os
import time

import requests
from bs4 import BeautifulSoup

API = "https://api.spotify.com/v1"
URL = "https://www.6play.fr/rtl2/quel-est-ce-titre"

token = os.getenv("token")
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

print("Run with")
print("Token        = " + token)
print("ClientId     = " + client_id)
print("ClientSecret = " + client_secret)
print(" ")


def get_token():
    query = requests.post("https://accounts.spotify.com/api/token", {
        "refresh_token": token,
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret
    }).json()

    return query["access_token"]


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


def get_track_id_spotify(music):
    query = "q=" + music + "&type=track"
    spotify = requests.get(API + "/search?" + query, headers={"Authorization": "Bearer " + get_token()})

    result = spotify.json()["tracks"]["items"]
    if len(result) > 0:
        return result[0]["uri"]

    return None


def track_already_exist(track):
    spotify = requests.get(API + "/playlists/6iazs8VECddcN2EtJFDhVA/tracks?market=FR&fields=items(track(uri))",
                           headers={"Authorization": "Bearer " + get_token()})
    exist = False

    for item in spotify.json()["items"]:
        if item["track"]["uri"] == track:
            exist = True

    return exist


def add_music_to_playlist(track):
    spotify = requests.post(API + "/playlists/6iazs8VECddcN2EtJFDhVA/tracks?uris=" + track,
                            headers={
                                "Authorization": "Bearer " + get_token()})
    print(spotify.json())


def run():
    print("Run at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    musics = get_last_music()

    for music in musics:
        track_id = get_track_id_spotify(music)

        if track_id is not None:
            if not track_already_exist(track_id):
                add_music_to_playlist(track_id)
        else:
            log = open("log.txt", "a")
            log.write("Can't find the music " + music)

    time.sleep(600)
    run()


run()
