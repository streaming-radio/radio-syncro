import requests
from bs4 import BeautifulSoup

from syncro.service.platform.Spotify import Spotify
from syncro.service.radio.BaseRadio import BaseRadio


class RadioRTL2(BaseRadio):
    def __init__(self, spotify: Spotify):
        """
        Create an instance of RadioNRJ

        :param spotify: The spotify client
        """
        super().__init__("RTL2", "6iazs8VECddcN2EtJFDhVA", spotify)

    def get_last_musics(self) -> list[list]:
        """
        Parsing and get the last music at the radio

        :return: a list of music at the format [[title, artist]]
        """
        page = requests.get("https://www.6play.fr/rtl2/quel-est-ce-titre")
        musics = []

        html_body = BeautifulSoup(page.content, "html.parser")
        html_music = html_body.findAll(class_="ecfper-4 dswJZp")

        for music in html_music:
            title = music.find(class_="ecfper-5 cLjpFE").text
            author = music.find(class_="ecfper-6 cLqSnv").text
            musics.append([title, author])

        return musics
