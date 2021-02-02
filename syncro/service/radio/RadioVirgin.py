import requests
from bs4 import BeautifulSoup

from syncro.service.radio.BaseRadio import BaseRadio


class RadioVirgin(BaseRadio):
    def __init__(self):
        super().__init__("VIRGIN", "5AOn63dCvPO3UP8FO9bgQz")

    def get_last_musics(self):
        page = requests.get("https://www.virginradio.fr/cetait-quoi-ce-titre/")
        musics = []

        html_body = BeautifulSoup(page.content, "html.parser")
        html_music = html_body.findAll(class_="inner _l")

        for music in html_music:
            title = music.find(class_="title").text
            author = music.find(class_="artist").text
            musics.append(title + " " + author)
        return musics
