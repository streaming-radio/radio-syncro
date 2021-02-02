from syncro.service.platform.Spotify import Spotify


class BaseRadio:
    def __init__(self, name: str, playlist: str, spotify: Spotify):
        """
        Create a new instance of BaseRadio

        :param name: the name of the radio
        :param playlist: the spotify playlist id
        :param spotify: the spotify client
        """
        self.__playlist = playlist
        self.__name = name
        self.__spotify = spotify

    def execute(self) -> None:
        """
        Run the synchro for the radio
        """
        print(self.__name + " Is Running ..")

        for music in self.get_last_musics():
            track_id = self.__spotify.get_track_id_spotify(music[0], music[1])

            if track_id is not None:
                if not self.__spotify.track_already_exist(track_id, self.__playlist, 0):
                    self.__spotify.add_music_to_playlist(track_id, self.__playlist)
                    print(self.__name + " Add : " + music[0] + " " + music[1])
                    # else:
                # log = open("log.txt", "a")
                # log.write("Can't find the music " + music + "\n")

    def get_last_musics(self) -> dict:
        pass
