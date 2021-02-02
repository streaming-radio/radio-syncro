import requests
from bs4 import BeautifulSoup

from syncro.service.radio.BaseRadio import BaseRadio


class RadioNRJ(BaseRadio):
    def __init__(self, spotify):
        super().__init__("NRJ", "67Bq7QEyqEzvQ9IKqH7QVO", spotify)

    def get_last_musics(self):
        page = requests.get("https://www.playlisteradio.com/nrj-radio")
        musics = []

        html_body = BeautifulSoup(page.content, "html.parser")
        html_music = html_body.findAll(class_="history-song")

        for music in html_music:
            title = music.find(class_="titre").text
            author = music.find(class_="artiste").text
            musics.append([title, author])
        return musics
