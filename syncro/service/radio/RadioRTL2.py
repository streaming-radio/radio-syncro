import requests
from bs4 import BeautifulSoup

from syncro.service.radio.BaseRadio import BaseRadio


class RadioRTL2(BaseRadio):
    def __init__(self):
        super().__init__("6iazs8VECddcN2EtJFDhVA")

    def get_last_musics(self):
        page = requests.get("https://www.6play.fr/rtl2/quel-est-ce-titre")
        musics = []

        html_body = BeautifulSoup(page.content, "html.parser")
        html_music = html_body.findAll(class_="ecfper-4 dswJZp")

        for music in html_music:
            title = music.find(class_="ecfper-5 cLjpFE").text
            author = music.find(class_="ecfper-6 cLqSnv").text
            musics.append(title + " " + author)

        return musics
