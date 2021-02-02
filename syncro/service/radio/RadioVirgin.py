import requests
from bs4 import BeautifulSoup

from syncro.service.platform.Spotify import Spotify
from syncro.service.radio.BaseRadio import BaseRadio


class RadioVirgin(BaseRadio):
    def __init__(self, spotify: Spotify):
        """
        Create an instance of RadioNRJ

        :param spotify: The spotify client
        """
        super().__init__("VIRGIN", "5AOn63dCvPO3UP8FO9bgQz", spotify)

    def get_last_musics(self):
        """
        Parsing and get the last music at the radio

        :return: a list of music at the format [[title, artist]]
        """
        page = requests.get("https://www.virginradio.fr/cetait-quoi-ce-titre/")
        musics = []

        html_body = BeautifulSoup(page.content, "html.parser")
        html_music = html_body.findAll(class_="inner _l")

        for music in html_music:
            title = music.find(class_="title").text
            author = music.find(class_="artist").text
            musics.append([title, author])
        return musics
