import requests
from bs4 import BeautifulSoup

from syncro.service.radio.BaseRadio import BaseRadio


class RadioNRJ(BaseRadio):
    def __init__(self):
        super().__init__("35neAy6GCJXLamNQqBqgnU")

    def get_last_musics(self):
        page = requests.get("https://www.nrj.fr/chansons-diffusees")
        musics = []

        html_body = BeautifulSoup(page.content, "html.parser")
        html_music = html_body.findAll(class_="cardPlaylist-body")

        print(html_body)

        for music in html_music:
            title = music.find(class_="description").text
            author = music.find(class_="heading4").text
            musics.append(title + " " + author)

        return musics
